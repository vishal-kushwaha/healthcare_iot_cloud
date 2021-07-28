""" custom datetime attribute """
from datetime import datetime

from pynamodb.attributes import UTCDateTimeAttribute


class MyUTCDateTimeAttribute(UTCDateTimeAttribute):
    """ custom datetime attribute; overrides serialization/deserialization """
    def deserialize(self, value):
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

    def serialize(self, value):
        return value.strftime("%Y-%m-%d %H:%M:%S")
