from ..models import CustomUser, Event, Vote
from django.db.models import F

def recommend_by_interest(user):
    recommendations = []
    events = Event.objects.all()
    for event in events:
        for tag in event.eventTags.all():
            if tag in user.userInterests.all() and event not in recommendations and event.num_attendees < event.range:
                recommendations.append(event)
                Vote.objects.filter(user=user).filter(event=event).update(interestScore = 1)
            elif tag in user.userInterests.all() and event in recommendations:
                Vote.objects.filter(user=user).filter(event=event).update(interestScore=F('interestScore') + 1)
    
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
                        Vote.objects.filter(user=user).filter(event=otherEvent).update(othersScore = 1)
                    elif otherEvent not in user.schedule.events.all() and otherEvent in recommendations:
                        Vote.objects.filter(user=user).filter(event=otherEvent).update(othersScore=F('othersScore') + 1)
