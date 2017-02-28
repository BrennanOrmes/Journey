# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from schedule import Schedule
from event import Event
from datetime import datetime
import pytz
#from .models import Events

def date(s):
    unaware = datetime.strptime(s,"%Y-%m-%dT%H:%M:%S")
    now_aware = pytz.utc.localize(unaware)
    return now_aware


# Test Data
"""
e1 = Event(title=u"Prototype Hackathon",
           location=u"MR311",
           description=u"Still need to finish the project, grab some red bull and get to work",
           start_time=date("2016-11-26T10:00:00"),
           end_time=date("2016-11-26T15:00:00"),
           #[u"project", u"procrastination"],
           price=0.00,
           public=True
           )

e2 = Event(title=u"Team Alpha Party",
           location=u"Ruben's House",
           description=u"We did it, time to drink. BYOB",
           start_time=date("2016-11-26T21:00:00"),
           end_time=date("2016-11-26T23:59:59"),
           #[u"project", u"drinking"],
           price=0.00,
           public=True
           )
e3 = Event(title=u"Software Engineering Practical",
           location=u"MR311",
           description=u"Present on what we did this week. Who wrote the presentation this time anyway? ",
           start_time=date("2016-11-21T11:00:00"),
           end_time=date("2016-11-21T12:00:00"),
           #[u"project", u"ernesto"],
           price=0.00,
           public=True
           )
e4 = Event(title=u"Slain's Pub Quiz",
           location=u"Slains Pub",
           description=u"Four rounds of pretty easy questions and a chance to win a £50 bar tab",
           start_time=date("2016-11-23T20:00:00"),
           end_time=date("2016-11-23T23:59:59"),
           #[u"quiz",u"drinking"],
           price=1.00,
           public=True
           )
e5 = Event(title=u"Operating Systems Hackathon",
           location=u"MR311",
           description=u"How do I debug C? I dunno, but this filesystem is getting done.",
           start_time=date("2016-11-26T11:00:00"),
           end_time=date("2016-11-26T18:00:00"),
           #[u"operating systems", u"procrastination"],
           price=0.00,
           public=True
           )
"""

# e1, e2, e3, e4, e5 = Event.objects.all()[:5]
#current_schedule = Schedule.objects.get(pk=5)
"""
current_schedule = Schedule()
current_schedule.save()
current_schedule.add_event(e2)
current_schedule.add_event(e3)
current_schedule.add_event(e4)
"""
user_tags = []
