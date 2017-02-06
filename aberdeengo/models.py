from django.db import models
from django.contrib.auth.models import User
#from .validators import UnicodeUsernameValidator

class CustomUser(User):
  #  username_validator = UnicodeUsernameValidator()
    payment = models.CharField(max_length=255)

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
    
class Tag(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Interests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
class EventTag(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

class LocationTag(models.Model):
    event = models.ForeignKey(Location, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

class ScheduleEntry(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.TimeField()
    end = models.TimeField()


class Event(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255) # models.ForeignKey(Location, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    public = models.BooleanField() # default true
    price = models.IntegerField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)

    tags = set([])
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

    def clashes_with(self, other):
        """Checks if this event overlaps with another event"""
        return (between(self.start_time, other.start_time, self.end_time)
                or between(other.start_time, self.start_time, other.end_time))

def between(x, y, z):
    "Returns true if x <= y <= z"
    return (x <= y) and (y <= z)
