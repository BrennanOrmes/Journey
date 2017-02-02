# -*- coding: utf-8 -*-
from datetime import datetime, timedelta


class Schedule(object):
    def __init__(self):
        """Create a Schedule"""
        self.event_map = {}

    def add_event(self, event):
        """Add an event to this schedule if possible. If it cannot be added,
        an EventsClash exception is thrown"""
        if event.id in self.event_map:
            return

        for e in self.event_map.values():
            if event.clashes_with(e):
                raise EventsClash(event, e)

        self.event_map[event.id] = event

    def remove_event(self, event):
        """Removes an event from this schedule"""
        self.event_map.pop(event.id, None)
        # delete without an exception on fail

    # TODO: necessary?
    def get_event(self, event_id):
        return self.event_map[event_id]

    def events_in_range(self, start, end):
        """Returns the events scheduled between the start and end dates"""
        return [event for event in self.events() if event.in_range(start, end)]

    def current_event(self):
        now = datetime.now()
        delta = timedelta(seconds=1)
        events = self.events_in_range(now, now + delta)
        if events == []:
            return False
        else:
            return events[0]

    def events(self):
        """Returns a list of all the events in this schedule"""
        # TODO: should we be deleting events that have already passed?
        return sorted(self.event_map.values(), key=lambda x: x.start_time)

    def save(self):
        pass


class EventsClash(Exception):
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
