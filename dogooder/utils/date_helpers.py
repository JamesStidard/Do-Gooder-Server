from datetime import datetime
import time

__author__ = 'James Stidard'


def parse_unix_time(value):
    return datetime.datetime.fromtimestamp(int(value))


def to_unix_time(value):
    value = time.mktime(value.timetuple())
    return value
