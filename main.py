""" this module depicts the solution for the project problem statements """
import logging
from datetime import datetime

from rules import Rule
from src import aggregate_data, record_alerts


def main():
    """ demonstrates the usage of functions """
    # logging configuration
    logging.basicConfig()
    log = logging.getLogger("pynamodb")
    log.setLevel(logging.DEBUG)
    log.propagate = True

    # lower and upper bounds for aggregate_data and record_alerts functions
    lower = datetime(year=2021, month=6, day=26, hour=5, minute=50)
    upper = datetime(year=2021, month=6, day=26, hour=6, minute=51)

    # calling aggregation with lower and upper bounds
    aggregate_data(lower, upper)

    # instantiate rules for alerts
    rules = list(map(Rule, ['rules/temperature.json', 'rules/spo2.json', 'rules/heart_rate.json']))
    # calling records_alerts with rules, lower and upper bound
    record_alerts(rules, lower, upper)


if __name__ == '__main__':
    main()
