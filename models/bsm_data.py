""" bsm_data model """
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.models import Model

from attributes import MyUTCDateTimeAttribute


class BsmData(Model):
    """ model for bsm_data model """
    class Meta:
        table_name = 'bsm_data'

    device_id = UnicodeAttribute(hash_key=True, attr_name='deviceid')
    timestamp = MyUTCDateTimeAttribute(range_key=True)
    datatype = UnicodeAttribute()
    value = NumberAttribute()
