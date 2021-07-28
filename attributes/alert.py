""" custom alert attribute """
from pynamodb.attributes import MapAttribute, UnicodeAttribute, NumberAttribute

from .rule import RuleAttribute


class AlertAttribute(MapAttribute):
    """ custom attribute for nesting multiple alerts for same device/timestamp combination """
    datatype = UnicodeAttribute()
    value = NumberAttribute()
    rule = RuleAttribute()
