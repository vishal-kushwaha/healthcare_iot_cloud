""" bsm_agg_data model """
from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model

from attributes import MyUTCDateTimeAttribute, DataAttribute


class BsmAggData(Model):
    """ model class for bsm_agg_data table """
    class Meta:
        table_name = 'bsm_agg_data'

    device_id = UnicodeAttribute(hash_key=True, attr_name='deviceid')
    timestamp = MyUTCDateTimeAttribute(range_key=True)
    data = DataAttribute()
