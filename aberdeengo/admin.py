'''
    admin.py - Registers models so they can be created from the admin interface.

    Author: Team Alpha

    Tested?: Yes
    Functional?: Yes
    Merged?: Yes
    Copyright: (c) 2017 Team Alpha, University of Aberdeen.
'''
from django.contrib import admin

from .models import CustomUser, Event, Tag, Ticket

admin.site.register(CustomUser)
admin.site.register(Event)
admin.site.register(Tag)
admin.site.register(Ticket)
