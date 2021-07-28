""" rule attribute """
from pynamodb.attributes import MapAttribute, UnicodeAttribute, NumberAttribute


class RuleAttribute(MapAttribute):
    """ custom attribute for rule """
    type = UnicodeAttribute()
    avg_min = NumberAttribute()
    avg_max = NumberAttribute()
    trigger_count = NumberAttribute()
