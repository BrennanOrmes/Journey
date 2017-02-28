from django.contrib import admin

from .models import CustomUser, Tag

admin.site.register(CustomUser)
admin.site.register(Tag)