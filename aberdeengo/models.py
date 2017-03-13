from django.db import models
from django.contrib.auth.models import User
import datetime
#from .validators import UnicodeUsernameValidator

class Tag(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class CustomUser(User):
    payment = models.CharField(max_length=255)
    # 'Schedule' needs to be the class name rather than the object to prevent errors
    schedule = models.OneToOneField('Schedule', null=True) # null is temporary
    interests = models.ManyToManyField(Tag)

class Location(models.Model):
    coordinates = models.FloatField(max_length=20) #momentarily not used
    name = models.CharField(max_length=255)
    opentime = models.TimeField(null=True)
    closedtime = models.TimeField(null=True)

class Events(models.Model):
    name = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    #location = models.ForeignKey(Location, on_delete=models.CASCADE)
    public = models.BooleanField()
    price = models.IntegerField(null=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    


class Interests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
class EventTag(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

class LocationTag(models.Model):
    event = models.ForeignKey(Location, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)



class Event(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255) # models.ForeignKey(Location, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    public = models.BooleanField() # default true
    price = models.IntegerField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    publication_date = models.DateField(("Date"), default=datetime.date.today)

    #tags = models.ManyToManyField(Tag)
    eventTags = models.ManyToManyField(Tag)
    # def add_tags(self, newentry):
    #     tags = self.tags.all()
    
    
    #cost
    # owner
    #wtf?? why are there two events classes????? <3 ruben

    def customise(self, start_time=False, end_time=False, transport=False):
        """Returns a customised object for this event"""
        c = Customised(self)
        c.change_times(start_time, end_time)
        c.change_transport(transport)
        return c

    @classmethod
    def search(self, string, tags):
        """Searches the database for an event that match the given string and
        tags."""

        results = []
        # TODO: reuse the django search functionality

        for event in Event.objects.all():
            if event.matches_string(string) and event.matches_tags(tags):
                results.append(event)
        return results

    @classmethod
    def find_by_id(self, id):
        return Event.objects.get(id=id)

    def matches_string(self, string):
        """Checks if this event matches a given search string"""
        # TODO: need a method for location
        return (string in self.title
                or string in self.description
                or string in self.location)

    def matches_tags(self, tags):
        """Checks if this event matches a given set of tags"""
        tags = set(tags)
        return not tags or tags.intersection(self.tags)



class Schedule(models.Model):
    events = models.ManyToManyField(Event, through = 'ScheduleEntry')
    def add_event(self, newentry):
        """Add an event to this schedule if possible. If it cannot be added,
        an EventsClash exception is thrown"""
        events = self.scheduleentry_set.all()
        
        if newentry.start == '':
            newentry.start = newentry.event.start_time
        if newentry.end == '':
            newentry.start = newentry.event.start_time
        #maybe put this in a different method to be called?
        #checking that scheduled time is consistent with event and itself
        if newentry.start > newentry.end:
            s = "implying you are leaving before going"
            raise InconsistentTime(newentry.event, s)
        elif newentry.start == newentry.end:
            raise InconsistentTime(newentry.event, "implying you are going and leaving at the same time")
        else:
            if newentry.start < newentry.event.start_time:
                raise InconsistentTime(newentry.event, "earlier than the event takes place")
            elif newentry.end > newentry.event.end_time:
                raise InconsistentTime(newentry.event, "later than the event takes place") #hack, it would be better if the error wasn't in the link. fix in another branch
     
        
        for e in events:
            if newentry.clashes_with(e):
                raise EventsClash(newentry.event, e)
        # when it clashes we could do a neat thing where a link appears that takes them to the schedule and scrolls down to the one that it clashes with (in another branch of course)

        newentry.save()

    def remove_event(self, event):
        """Removes an event from this schedule"""
        event.delete()
        # delete without an exception on fail # I will probably move this in scheduleentry

    def events_in_range(self, start, end):
        """Returns the events scheduled between the start and end dates"""
        return [event for event in self.events.all() if event.in_range(start, end)]

    def current_event(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(seconds=1)
        events = self.events_in_range(now, now + delta)
        if events == []:
            return False
        else:
            return events[0]

    def scheduled_events(self):
        """Returns a list of all the events in this schedule"""
        # TODO: should we be deleting events that have already passed? No, we should just not display them. It's good to have them in the database for statistics
        return sorted(self.scheduleentry_set.all(), key=lambda x: x.start)

class ScheduleEntry(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    travelType = models.CharField(max_length=255, default="DRIVING")
    
    def clashes_with(self, other):
        """Checks if this event overlaps with another event"""
        return (between(self.start, other.start, self.end)
            or between(other.start, self.start, other.end))
    
    @classmethod
    def find_by_id(self, id):
        return ScheduleEntry.objects.get(id=id)

class EventsClash(Exception):
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2


class InconsistentTime(Exception):
    def __init__(self,e1,e2):
        self.e1 = e1
        self.e2 = e2


def between(x, y, z):
    "Returns true if x <= y <= z"
    return (x < y) and (y < z)
