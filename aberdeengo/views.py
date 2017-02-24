from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from scripts.event import Event
from scripts.schedule import Schedule, EventsClash
from scripts.test import user_tags, date
from scripts.signup import *

from .models import CustomUser

# Create your views here. --> WHOOP

def home(request):
    return render(request,'index.html')
    
def contact(request):
    return render(request,'contact.html')
    
def searchEvents(request):
    search_string = request.GET.get("q",'')
    events = Event.search(search_string, user_tags) #TODO: add limiting
    events.sort(key=lambda x: x.start_time)
    template = loader.get_template('search.html')
    if request.user.is_anonymous():
        scheduled_events = []
    else:
        user = CustomUser.objects.get(username=request.user.username)
        scheduled_events = user.schedule.scheduled_events()
    context = {
        'events': events,
        'scheduled_events' : scheduled_events
    }
    return HttpResponse(template.render(context,request))

@login_required
def schedule(request):
    template = loader.get_template('schedule.html')
    user = CustomUser.objects.get(username=request.user.username)
    context = RequestContext(request, {
        'schedule' : user.schedule
    })
    return HttpResponse(template.render(context,request))
    


def event(request,id):
    event = Event.find_by_id(int(id))
    clashes = request.GET.get('clash')
    if clashes:
        clashes = Event.find_by_id(int(clashes))
    
    template = loader.get_template('search.html')
    # Will need to split out the veent part of the search template so that we don't get "clashes" appearing everywhere
    if request.user.is_anonymous():
        scheduled_events = []
    else:
        user = CustomUser.objects.get(username=request.user.username)
        scheduled_events = user.schedule.scheduled_events()
    context = RequestContext(request, {
        'events': [event],
        'clashes' : clashes,
        'scheduled_events' : scheduled_events
    })
    return HttpResponse(template.render(context,request))
@login_required
def addEvent(request):
    if request.method == "POST":
        # TODO: check fields
        title = request.POST.get('title','')
        location = request.POST.get('location','')
        description = request.POST.get('description','')
        start_time = date(request.POST.get('startdate',''))
        end_time = date(request.POST.get('enddate',''))
        currentUsername = request.user.username
        user = CustomUser.objects.get(username=currentUsername)
        tags = []
        cost = 0
        public = True
        e = Event(title=title, start_time=start_time, end_time=end_time, location=location, description=description, public=public, price=cost, user=user)
        e.save()
        return redirect('event', e.id)
    else:
        template = loader.get_template('addevent.html')
        context = RequestContext(request,{})
        return HttpResponse(template.render(context,request))

@login_required
def schedule_event(request):
    user = CustomUser.objects.get(username=request.user.username)
    if request.method == "POST":
        event_id = int(request.POST.get('event_id'))
        event = Event.find_by_id(event_id)
        if request.POST.get('schedule') == '1':
            try:
                user.schedule.add_event(event)
                return redirect('schedule')
            except EventsClash as e:
                return redirect(reverse('event', args=[event_id]) + '?clash={}'.format(e.e2.id)) # hack
        else:
            user.schedule.remove_event(event)
            return redirect('schedule')
    else:
        raise Http404("Page not found")
        
def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            s = Schedule()
            s.save()
            user = CustomUser.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email'],
            payment = 'none',
            schedule = s
            )
            return redirect('login')
        else:
            messages.error(request, "Error")
    else:
        template = loader.get_template('signup.html')
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'signup.html',
    variables,
    )

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return render(request,'index.html')
    
    elif request.user.is_authenticated():
        return render(request,'logout.html')
    else:
        return redirect(login)

@login_required()
def accounts(request, username):
    currentUsername = request.user.username
    currentUser = CustomUser.objects.get(username=currentUsername)
    events = Event.objects.filter(user=currentUser).order_by('publication_date') 
    context = {
        'user': currentUser,
        'events': events
    }
    if request.user.is_authenticated():
        template = loader.get_template('accounts.html')
        return HttpResponse(template.render(context, request))
    else: 
        return redirect(login)
    
    
def editAccount(request):
    return render(request,'ajax/profile.html')

def ownedEvents(request):
    return render(request,'ajax/events.html')
    
def interests(request):
    return render(request,'ajax/interests.html')