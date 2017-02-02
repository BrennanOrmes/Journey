from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from scripts.event import Event
from scripts.schedule import Schedule
from scripts.test import current_schedule

# Create your views here.

def home(request):
    return render(request,'index.html')
    
def searchEvents(request):
    request.GET
    events = Event.search("string", ["tag1"])
    template = loader.get_template('search.html')
    context = {
        'events': events
    }
    return HttpResponse(template.render(context,request))
    
def schedule(request):
    template = loader.get_template('schedule.html')
    context = {
        'schedule' : current_schedule
    }
    return HttpResponse(template.render(context,request))
    
def contact(request):
    return render(request,'contact.html')

def event(request,id):
    event = Event.find_by_id(int(id))
    template = loader.get_template('search.html')
    context = {
        'events': [event]
    }
    return HttpResponse(template.render(context,request))