from ..models import CustomUser, Event, Vote
from django.db.models import F
import operator

'''
    recommendations.py - Provides the recommendation algorithms
    used in views.py to generate events to be recommended
    to each user
    
    Author: Team Alpha                                                                          
    
    Tested?: Yes
    Functional?: Yes
    Merged?: Yes
    Copyright: (c) 2016 Team Alpha, University of Aberdeen.
'''    
    
'''
recommendations by interest: compares the user's interests with the
tags of each event and produces a score for each event based on this.
The bigger the overlap between tags and interests, the bigger the
score that an event get will be.
'''
def recommend_by_interest(user):
    recommendations = []
    events = Event.objects.all()
    for event in events:
        for tag in event.eventTags.all():
            if tag in user.userInterests.all() and event not in recommendations and event.num_attendees < event.range:
                recommendations.append(event)
                Vote.objects.filter(user=user).filter(event=event).update(interestScore=1)
            elif tag in user.userInterests.all() and event in recommendations:
                Vote.objects.filter(user=user).filter(event=event).update(interestScore=F('interestScore') + 1)

'''
recommendations by what other users have visited: check for each event
that a user has visited, for other users that have visited the same
event, check what other events they have visited that the initial
user has not visited and increment their score based on this.
'''
def recommend_by_other_users(user):
    recommendations = []
    events = user.schedule.events.all()
    otherUsers = CustomUser.objects.all()
    for event in events:
        for otherUser in otherUsers:
            if event in otherUser.schedule.events.all():
                for otherEvent in otherUser.schedule.events.all():
                    if otherEvent not in user.schedule.events.all() and otherEvent not in recommendations and otherEvent.num_attendees < otherEvent.range:
                        recommendations.append(otherEvent)
                        Vote.objects.filter(user=user).filter(event=otherEvent).update(othersScore=1)
                    elif otherEvent not in user.schedule.events.all() and otherEvent in recommendations:
                        Vote.objects.filter(user=user).filter(event=otherEvent).update(othersScore=F('othersScore') + 1)


'''
featured events: produces a sorted list of all the public
events based on the difference between the range of visitors
that an event needs to reach and the visitors already attending,
so that events which still need a lot of people to add them to
their schedules are displayed first
'''
def featured():
    featuredevents = []
    events = Event.objects.all()
    for event in events:
        if event.public is True:
            featuredevents.append((event, event.num_attendees() - event.range))
    featuredevents = sorted(featuredevents, key=lambda x: x[1])
    events = []
    for event in featuredevents:
            events.append(event[0])
    return events
