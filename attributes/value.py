""" custom value attribute """
from pynamodb.attributes import MapAttribute, NumberAttribute


class ValueAttribute(MapAttribute):
    """ custom attribute for nesting the data """
    min = NumberAttribute()
    max = NumberAttribute()
    avg = NumberAttribute()
