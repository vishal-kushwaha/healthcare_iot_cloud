""" bsm_alerts model """
from pynamodb.attributes import UnicodeAttribute, ListAttribute
from pynamodb.models import Model

from attributes import MyUTCDateTimeAttribute, AlertAttribute


class BsmAlert(Model):
    """ model for  bsm_alerts table """
    class Meta:
        table_name = 'bsm_alerts'

    device_id = UnicodeAttribute(hash_key=True, attr_name='deviceid')
    timestamp = MyUTCDateTimeAttribute(range_key=True)
    alerts = ListAttribute(of=AlertAttribute)
