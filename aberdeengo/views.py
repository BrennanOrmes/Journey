from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
from scripts.event import Event
from scripts.schedule import Schedule, EventsClash
from scripts.test import current_schedule, user_tags, date
from .models import CustomUser


from scripts.signup import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.contrib import messages
from django.http import Http404


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
        
# def signup(request):
#     if request.method == "POST":
#         # TODO: check fields
#         email = request.POST.get('email','')
#         username = request.POST.get('username','')
#         password1 = request.POST.get('password1','')
#         password2 = request.POST.get('password2','')
#         if password1 == password2:
#             u = CustomUser(email=email,username=username, password=password1,payment="paypal")
#             u.save()
#             return redirect('contact')
#         else:
#             return redirect('signup')
#     else:
#         template = loader.get_template('signup.html')
#         context = RequestContext(request,{})
#         return HttpResponse(template.render(context,request))

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email'],
            payment = 'none'
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
    

from django.contrib.auth import authenticate
from django.contrib import auth
# user = authenticate(username='john', password='secret')
# if user is not None:
#     # A backend authenticated the credentials
# else:
#     # No backend authenticated the credential
# and not request.user.is_authenticated()
  
# def login(request):
#     if request.method == 'POST':
#         u = request.POST.get('username','')
#         p = request.POST.get('password','')
#         user = authenticate(username=u, password=p)
#         if user is not None:
#             auth.login(request, user)
#             #return redirect('contact')
#             return redirect('user', user.username) #this will redirect you to your account page once you log in
#         else:
#             return redirect('signup')   
#     else:
#             if request.user.is_authenticated():
#                  return render(request,'logout.html')
#             else:
#                 return render(request,'login.html')
                
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
    #u = User.find_by_id(int(id))
    #u = User.objects.get(username=username)
    #return redirect('user', username)
    #return render(request, 'index.html')
    currentUsername = request.user.username
    currentUser = CustomUser.objects.get(username=currentUsername)
    event = Event.objects.get(user=currentUser)
    if request.user.is_authenticated():
        return render(request, 'accounts.html', {'user' : currentUser, 'event' : event})
    else: 
        return redirect(login)