from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
from scripts.event import Event
from scripts.schedule import Schedule, EventsClash
from scripts.test import current_schedule, user_tags, date
from .models import User

# Create your views here.

def home(request):
    return render(request,'index.html')
    
def contact(request):
    return render(request,'contact.html')
    
def searchEvents(request):
    search_string = request.GET.get("q",'')
    events = Event.search(search_string, user_tags) #TODO: add limiting
    events.sort(key=lambda x: x.start_time)
    template = loader.get_template('search.html')
    context = {
        'events': events,
        'scheduled_events' : current_schedule.events()
    }
    return HttpResponse(template.render(context,request))
    
def schedule(request):
    template = loader.get_template('schedule.html')
    context = RequestContext(request, {
        'schedule' : current_schedule
    })
    return HttpResponse(template.render(context,request))
    


def event(request,id):
    event = Event.find_by_id(int(id))
    clashes = request.GET.get('clash')
    if clashes:
        clashes = Event.find_by_id(int(clashes))
    
    template = loader.get_template('search.html')
    # Will need to split out the veent part of the search template so that we don't get "clashes" appearing everywhere
    context = RequestContext(request, {
        'events': [event],
        'clashes' : clashes,
        'scheduled_events' : current_schedule.events()
    })
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
        e = Event(title=title, start_time=start_time, end_time=end_time, location=location, description=description, public=public, price=cost)
        e.save()
        return redirect('event', e.id)
    else:
        template = loader.get_template('addevent.html')
        context = RequestContext(request,{})
        return HttpResponse(template.render(context,request))

def schedule_event(request):
    if request.method == "POST":
        event_id = int(request.POST.get('event_id'))
        event = Event.find_by_id(event_id)
        if request.POST.get('schedule') == '1':
            try:
                current_schedule.add_event(event)
                return redirect('schedule')
            except EventsClash as e:
                return redirect(reverse('event', args=[event_id]) + '?clash={}'.format(e.e2.id)) # hack
        else:
            current_schedule.remove_event(event)
            return redirect('schedule')
    else:
        raise Http404("Page not found")
        
def signup(request):
    if request.method == "POST":
        # TODO: check fields
        email = request.POST.get('email','')
        username = request.POST.get('username','')
        password1 = request.POST.get('password1','')
        password2 = request.POST.get('password2','')
        if password1 == password2:
            u = User(email=email,username=username, password=password1,payment="paypal")
            u.save()
            return redirect('contact')
        else:
            return redirect('signup')
    else:
        template = loader.get_template('signup.html')
        context = RequestContext(request,{})
        return HttpResponse(template.render(context,request))
    
def login(request):
    return render(request,'login.html')
    
def user(request):
    return render(request, 'user.html')