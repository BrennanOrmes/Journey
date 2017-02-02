# -*- coding: utf-8 -*-
from ..models import Event

class Customised(object):
    def __init__(self, event):
        self.event = event
        self.transport = False
        self.times = False
        self.start_time = event.start_time
        self.end_time = event.end_time

    def change_times(self, start_time, end_time):
        # TODO: customised will need to refer to the event, so that
        # it can check for clashes
        if start_time > end_time:
            raise Exception  # TODO: what kind?
        if not between(self.event.start_time, start_time, self.event.end_time):
            raise Exception  # TODO: what kind?
        if not between(self.event.start_time, end_time, self.event.end_time):
            raise Exception  # TODO: what kind?
        self.start_time = start_time
        self.end_time = end_time

    # TODO: unnecessary?
    def change_transport(self, transport):
        self.transport = transport

    def save(self):
        pass

    def matches_string(self, string):
        return self.event.matches_string(string)

    def matches_tags(self, tags):
        return self.event.matches_tags(tags)

    def clashes_with(self, other):
        """Checks if this event overlaps with another event"""
        return (between(self.start_time, other.start_time, self.end_time)
                or between(other.start_time, self.start_time, other.end_time))


    def between(x, y, z):
        "Returns true if x <= y <= z"
        return (x <= y) and (y <= z)
