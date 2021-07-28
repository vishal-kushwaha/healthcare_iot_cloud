"""This module holds the functions for aggregation and alert processing"""
import time

import numpy as np
import pandas as pd

from models import BsmData, BsmAggData, BsmAlert
from attributes import DataAttribute, ValueAttribute, AlertAttribute, RuleAttribute
from rules import Rule


def _aggregate_data(data):
    """ aggregate data per device per sensor per minute """
    dataframe = pd.DataFrame(data, columns=['device_id', 'timestamp', 'datatype', 'value'])
    dataframe['interval'] = dataframe['timestamp']. \
        apply(lambda x: x.replace(second=0, microsecond=0))
    dataframe = dataframe.groupby(['device_id', 'datatype', 'interval']) \
        .agg([np.min, np.max, np.mean]) \
        .reset_index()
    return dataframe


def _assess_alerts(data, rules):
    """ assess data against rules """
    dataframe = pd.DataFrame(
        data,
        columns=['device_id', 'timestamp', 'HeartRate', 'SPO2', 'Temperature']
    )
    for rule in rules:
        event_column = f'{rule.type}_event'
        crossing_column = f'{rule.type}_crossing'
        count_column = f'{rule.type}_count'
        dataframe[event_column] = dataframe[rule.type].apply(rule)
        dataframe[crossing_column] = (dataframe[event_column] != dataframe[event_column].
                                      shift()).cumsum()
        dataframe[count_column] = dataframe.groupby([event_column, crossing_column]). \
                                      cumcount(ascending=False) + 1
        dataframe.loc[dataframe[event_column] == False, count_column] = 0
        dataframe[count_column] = dataframe[count_column].apply(lambda x: x == rule.trigger_count)
    return dataframe


def _bulk_write_bsm_agg_data(data):
    """ bulk write data to bsm_agg_data table """
    # create table if doesn't exist
    if not BsmAggData.exists():
        BsmAggData.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

    with BsmAggData.batch_write() as batch:
        for name, item in data:
            item.reset_index(inplace=True)
            data = DataAttribute(
                temperature=ValueAttribute(
                    min=item.iloc[2, 4],
                    max=item.iloc[2, 5],
                    avg=item.iloc[2, 6]
                ),
                heart_rate=ValueAttribute(
                    min=item.iloc[0, 4],
                    max=item.iloc[0, 5],
                    avg=item.iloc[0, 6]
                ),
                spo2=ValueAttribute(
                    min=item.iloc[1, 4],
                    max=item.iloc[1, 5],
                    avg=item.iloc[1, 6]
                )
            )
            entry = BsmAggData(device_id=name[0], timestamp=name[1], data=data)
            batch.save(entry)
            time.sleep(0.5)


def _get_rule_attribute(rule_path):
    rule = Rule(rule_path)
    return RuleAttribute(
        type=rule.type,
        avg_min=rule.min_avg,
        avg_max=rule.max_avg,
        trigger_count=rule.trigger_count
    )


def _bulk_write_bsm_alert_data(data):
    """ bulk write data to bsm_alerts table """
    # create table if doesn't exist
    if not BsmAlert.exists():
        BsmAlert.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

    with BsmAlert.batch_write() as batch:
        for _, event_item in data:
            alert_items = []
            if event_item['Temperature_count']:
                alert_items.append(AlertAttribute(
                    datatype='Temperature',
                    value=event_item['Temperature'],
                    rule=_get_rule_attribute('rules/temperature.json'))
                )
            if event_item['SPO2_count']:
                alert_items.append(AlertAttribute(
                    datatype='SPO2',
                    value=event_item['SPO2'],
                    rule=_get_rule_attribute('rules/spo2.json'))
                )
            if event_item['HeartRate_count']:
                alert_items.append(AlertAttribute(
                    datatype='HeartRate',
                    value=event_item['HeartRate'],
                    rule=_get_rule_attribute('rules/heart_rate.json'))
                )
            if alert_items:
                alert = BsmAlert(
                    device_id=event_item['device_id'],
                    timestamp=event_item['timestamp'],
                    alerts=alert_items
                )
                print('*'*10, alert.serialize())
                batch.save(alert)
                time.sleep(0.5)


def aggregate_data(lower=None, upper=None):
    """ aggregates the data from bsm_data table to bsm_agg_data table """
    # get data from the table based on the date range
    filter_condition = BsmData.timestamp.between(lower, upper) if all([lower, upper]) else None

    # generator expression for extracting the data from DynamoDB
    data = ((item.device_id, item.timestamp, item.datatype, item.value)
            for item in BsmData.scan(filter_condition=filter_condition))

    # aggregate data based on per minute resolution
    dataframe = _aggregate_data(data)

    # dump aggregated data to DynamoDB table; this context manager batches upto 25 put requests
    _bulk_write_bsm_agg_data(dataframe.groupby(['device_id', 'interval']))


def record_alerts(rules, lower=None, upper=None):
    """ assesses aggregated data against the list of rules; alerts are written to db """
    # get data from the table based on the date range
    filter_condition = BsmAggData.timestamp.between(lower, upper) if all([lower, upper]) else None

    # generator expression for extracting the data from DynamoDB
    data = ((
        item.device_id,
        item.timestamp,
        item.data.heart_rate.avg,
        item.data.spo2.avg, item.data.temperature.avg
    ) for item in BsmAggData.scan(filter_condition=filter_condition))

    # extract the indices for fifth consecutive occurrence of condition specified by rule
    dataframe = _assess_alerts(data, rules)

    # dump alerts data to DynamoDB table; this context manager batches upto 25 put requests
    _bulk_write_bsm_alert_data(dataframe.iterrows())
