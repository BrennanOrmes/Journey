# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from schedule import Schedule
from event import Event
from datetime import datetime
#from .models import Events

def date(s):
    return datetime.strptime(s,"%Y-%m-%dT%H:%M:%S")

## Create some events
e1 = Event(1,
           u"Prototype Hackathon",
           u"MR311",
           u"Still need to finish the project, grab some red bull and get to work",
           date("2016-11-26T10:00:00"),
           date("2016-11-26T15:00:00"),
           [u"project", u"procrastination"],
           0.00
           )
dbe1 = Ev()
e2 = Event(2,
           u"Team Alpha Party",
           u"Ruben's House",
           u"We did it, time to drink. BYOB",
           date("2016-11-26T21:00:00"),
           date("2016-11-26T23:59:59"),
           [u"project", u"drinking"],
           0.00
           )
e3 = Event(3,
           u"Software Engineering Practical",
           u"MR5",
           u"We haven't done the work. Please don't hurt us.",
           date("2016-11-21T11:00:00"),
           date("2016-11-21T12:00:00"),
           [u"project", u"ernesto"],
           0.00
           )
e4 = Event(4,
           u"Slain's Pub Quiz",
           u"Slains Pub",
           u"Four rounds of pretty easy questions and a chance to win a £50 bar tab",
           date("2016-11-23T20:00:00"),
           date("2016-11-23T23:59:59"),
           [u"quiz",u"drinking"],
           1.00
           )
e5 = Event(5,
           u"Operating Systems Hackathon",
           u"MR311",
           u"File Systems? What are those?",
           date("2016-11-26T11:00:00"),
           date("2016-11-26T18:00:00"),
           [u"operating systems", u"procrastination"],
           0.00
           )

current_schedule = Schedule()
current_schedule.add_event(e2)
current_schedule.add_event(e3)
current_schedule.add_event(e4)

user_tags = []
id_count = 10 # FIXME: should be added automatically by model