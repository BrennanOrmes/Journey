from django import template
from aberdeengo.models import *
from datetime import datetime
register = template.Library()


@register.filter(name='return_travel_type')
def return_travel_type(value, arg):
    return value[arg - 1].travelType


@register.filter(name='return_time_start')
def return_time_start(value, arg):
    return value[arg - 1].start


@register.filter(name='return_time_previous_end')
def return_time_previous_end(value, arg):
    return value[arg - 2].end
