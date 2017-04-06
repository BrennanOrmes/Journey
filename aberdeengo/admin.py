from django.contrib import admin

from .models import CustomUser, Event, Tag, Ticket

admin.site.register(CustomUser)
admin.site.register(Event)
admin.site.register(Tag)
admin.site.register(Ticket)
