""" custom data attribute """
from pynamodb.attributes import MapAttribute

from attributes.value import ValueAttribute


class DataAttribute(MapAttribute):
    """ custom data attribute for nesting the values """
    temperature = ValueAttribute(attr_name='Temperature', null=True)
    heart_rate = ValueAttribute(attr_name='HeartRate', null=True)
    spo2 = ValueAttribute(attr_name='SPO2', null=True)
