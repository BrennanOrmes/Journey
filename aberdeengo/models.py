'''
    models.py - Django ORM Classes

    Author: Team Alpha

    Tested?: Yes
    Functional?: Yes
    Merged?: Yes
    Copyright: (c) 2016, 2017 Team Alpha, University of Aberdeen.
'''
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.utils import timezone
import datetime
from aberdeengo import settings


class Tag(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def num_events(self):
        return self.event_set.count()


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if 'schedule' not in extra_fields:
            s = Schedule()
            s.save()
            extra_fields['schedule'] = s
        return super(CustomUserManager, self)._create_user(username, email, password, **extra_fields)


class CustomUser(User):
    objects = CustomUserManager()  # overrides manager

    payment = models.CharField(max_length=255)
    # 'Schedule' needs to be the class name rather than the object to prevent errors
    schedule = models.OneToOneField('Schedule', null=True)  # null is temporary
    profilePicture = models.ImageField('pictures/profile/%Y/%m/%d', null=True)
    userInterests = models.ManyToManyField(Tag)

    def is_active2(self):
        # should we be using the regular django is_active?
        return self.num_created() > 0 or self.num_attending() > 0

    def num_created(self):
        return self.event_set.count()

    def num_attending(self):
        return self.schedule.events.count()

    def is_new(self):
        threshold = datetime.timedelta(days=7)
        return (timezone.now() - self.date_joined) < threshold


class Location(models.Model):
    coordinates = models.FloatField(max_length=20)  # momentarily not used
    name = models.CharField(max_length=255)
    opentime = models.TimeField(null=True)
    closedtime = models.TimeField(null=True)


class Events(models.Model):
    name = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    # location = models.ForeignKey(Location, on_delete=models.CASCADE)
    public = models.BooleanField()
    price = models.IntegerField(null=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
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


class GroupOfEvents(models.Model):
    title = models.CharField(max_length=255)


class Event(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)  # models.ForeignKey(Location, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, default='')
    public = models.BooleanField(default=False)
    price = models.FloatField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    publication_date = models.DateField(("Date"), default=datetime.date.today)
    range = models.IntegerField(default=0)
    max_tickets = models.IntegerField(default=0)
    sold_tickets = models.IntegerField(default=0)
    recurrence = models.IntegerField(default=0)
    times = models.IntegerField(default=1)
    group = models.ForeignKey(GroupOfEvents, default=0)

    # tags = models.ManyToManyField(Tag)
    eventTags = models.ManyToManyField(Tag)
    # def add_tags(self, newentry):
    #     tags = self.tags.all()

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

    def is_attended(self):
        return self.num_attendees() > 0

    def num_attendees(self):
        return self.schedule_set.count()


class RecurrentEventManager(models.Manager):
    def get_query_set(self):
        return self.filter(recurrence__gt=1)


class RecurrentEvent(Event):
    class Meta:
        proxy = True
    objects = RecurrentEventManager()


class EventOccurence(models.Model):
    event = models.ForeignKey(Event)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Ticket(models.Model):
    user = models.ForeignKey(CustomUser, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True)
    code = models.CharField(max_length=255)


class Vote(models.Model):
    user = models.ForeignKey(CustomUser)
    event = models.ForeignKey(Event)
    interestScore = models.IntegerField(default=0)
    othersScore = models.IntegerField(default=0)


class Schedule(models.Model):
    events = models.ManyToManyField(Event, through='ScheduleEntry')

    def add_event(self, newentry):
        """Add an event to this schedule if possible. If it cannot be added,
        an EventsClash exception is thrown"""
        events = self.scheduleentry_set.all()

        if newentry.start == '':
            newentry.start = newentry.event.start_time
        if newentry.end == '':
            newentry.start = newentry.event.start_time
        # maybe put this in a different method to be called?
        # checking that scheduled time is consistent with event and itself
        if newentry.start > newentry.end:
            s = "implying you are leaving before going"
            raise InconsistentTime(newentry.event, s)
        elif newentry.start == newentry.end:
            raise InconsistentTime(newentry.event, "implying you are going and leaving at the same time")
        else:
            if newentry.start < newentry.event.start_time:
                raise InconsistentTime(newentry.event, "earlier than the event takes place")
            elif newentry.end > newentry.event.end_time:
                # hack, it would be better if the error wasn't in the link. fix in another branch
                raise InconsistentTime(newentry.event, "later than the event takes place")

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

    def scheduled_events(self,all=False):
        """Returns a list of scheduled events.
        If keyword argument all is True, then all events that have been
        scheduled are included. By default, only the events that have not
        passed are included.
        """
        now = datetime.datetime.now()
        events = self.scheduleentry_set.filter(end__gte=now)
        return sorted(events, key=lambda x: x.start)


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
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2


def between(x, y, z):
    "Returns true if x <= y <= z"
    return (x < y) and (y < z)


class Summary(models.Model):
    updated = models.DateTimeField(auto_now=True)
    num_events = models.IntegerField()
    num_attended = models.IntegerField()
    most_attended = models.ForeignKey(Event)
    num_active = models.IntegerField()
    new_users = models.IntegerField(default=0)

    @classmethod
    def most_recent(self, force=False):
        retval = Summary.objects.order_by('-updated').first()
        if retval is None and force:
            return Summary.now()
        else:
            return retval

    @classmethod
    def now(self):
        s = Summary()
        s.num_events = s._num_events()
        s.num_attended = s._num_attended()
        s.most_attended = s._most_attended()
        s.num_active = s._num_active()
        s.new_users = s._new_users()
        s.save()
        s._summarise_events()
        s._summarise_tags()
        s.save()  # needed?
        return s

    def _num_events(self):
        return Event.objects.count()

    def _num_attended(self):
        return len([event for event in self._events() if event.is_attended()])

    def _most_attended(self):
        return max(self._events(), key=lambda x: x.num_attendees())

    def _num_active(self):
        return len([user for user in self._users() if user.is_active2()])

    def _new_users(self):
        return (len([user for user in self._users() if user.is_new()]))

    def _events(self):
        return Event.objects.all()

    def _users(self):
        return CustomUser.objects.all()

    def _tags(self):
        return Tag.objects.all()

    def _summarise_events(self):
        for event in self._events():
            n = event.num_attendees()
            event_summary = EventSummary(event=event, num_attendees=n, summary=self)
            event_summary.save()

    def _summarise_tags(self):
        for tag in self._tags():
            n = tag.num_events()
            tag_summary = TagSummary(tag=tag, num_events=n, summary=self)
            tag_summary.save()


class TagSummary(models.Model):
    # Nulls are temporary
    updated = models.DateTimeField(auto_now=True)
    tag = models.ForeignKey(Tag, null=True)
    num_events = models.IntegerField(default=0)
    summary = models.ForeignKey(Summary, null=True)


class EventSummary(models.Model):
    updated = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(Event, null=True)  # temporary
    num_attendees = models.IntegerField(default=0)
    summary = models.ForeignKey(Summary, null=True)

# class UserSummary(models.Model):
#     updated = models.DateTimeField(auto_now=True)
#     user = models.ForeignKey(CustomUser)
#     summary = models.ForeignKey(Summary)
