from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, RequestContext

from scripts.event import Event
from scripts.schedule import Schedule
from scripts.test import current_schedule, user_tags, date

# Create your views here.

def home(request):
    return render(request,'index.html')
    
def searchEvents(request):
    search_string = request.GET.get("q",'')
    events = Event.search(search_string, user_tags, limit=10)
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

def addEvent(request):
    if request.method == "POST":
        # TODO: check fields
        title = request.POST.get('title','')
        location = request.POST.get('location','')
        description = request.POST.get('description','')
        start_time = date(request.POST.get('startdate',''))
        end_time = date(request.POST.get('enddate',''))
        tags = []
        cost = 0
        public = True
        id_count += 1
        e = Event(id_count, title, location, description, start_time, end_time, tags, cost, public)
        print e
        return redirect('event', id_count)
    else:
        template = loader.get_template('addevent.html')
        context = RequestContext(request,{})
        return HttpResponse(template.render(context,request))