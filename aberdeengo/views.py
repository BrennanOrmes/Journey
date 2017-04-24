'''
    views.py - Generates Responses to Http Requests.

    Author: Team Alpha

    Tested?: Yes
    Functional?: Yes
    Merged?: Yes
    Copyright: (c) 2016, 2017 Team Alpha, University of Aberdeen.
'''
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.crypto import get_random_string

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.ipn.signals import payment_was_successful
from datetime import timedelta

from scripts.event import Event
from scripts.test import user_tags, date
from scripts.social import get_social_context

from .models import *

from scripts.recommendations import recommend_by_interest, recommend_by_other_users, featured


from scripts.signup import *

# Create your views here. --> WHOOP


@csrf_exempt
def home(request):
    if request.user.is_anonymous():
        events = []
        events = featured()
        template = loader.get_template('index.html')
        context = RequestContext(request, {
            'events': events
        })
        return HttpResponse(template.render(context, request))
    else:
        currentUsername = request.user.username
        currentUser = CustomUser.objects.get(username=currentUsername)
        print "WAZ", type(currentUser), currentUsername, currentUser.schedule
        Vote.objects.filter(user=currentUser).delete()
        for event in Event.objects.all():
            v = Vote(user=currentUser, event=event, interestScore=0, othersScore=0)
            v.save()
        recommend_by_interest(currentUser)
        recommend_by_other_users(currentUser)
        votes = Vote.objects.filter(user=currentUser)
        events_by_interest = []
        events_by_other_users = []
        votes = votes.order_by('interestScore').reverse()
        voteInterest = votes.order_by('interestScore').reverse()

        for vote in votes:
            for event in Event.objects.all():
                if vote.event == event and vote.interestScore is not 0:
                    events_by_interest.append(event)

        votes = votes.order_by('othersScore').reverse()
        voteOthers = votes.order_by('interestScore').reverse()

        for vote in votes:
            for event in Event.objects.all():
                if vote.event == event and vote.othersScore is not 0 and vote.interestScore == 0:
                    events_by_other_users.append(event)

        v = Vote.objects.all()
        featuredEvents = []
        featuredEvents = featured()
        template = loader.get_template('index.html')
        context = RequestContext(request, {
            'events_by_interest': events_by_interest,
            'events_by_other_users': events_by_other_users,
            'votes': votes,
            'voteInterest': voteInterest,
            'voteOthers': voteOthers,
            'featuredEvents': featuredEvents,
            'v': v
        })
        return HttpResponse(template.render(context, request))


def contact(request):
    return render(request, 'contact.html')


def searchEvents(request):
    search_string = request.GET.get("q", '')
    events = Event.search(search_string, user_tags)  # TODO: add limiting
    events.sort(key=lambda x: x.start_time)
    template = loader.get_template('search.html')
    context = RequestContext(request, {
        'events': events
    })
    return HttpResponse(template.render(context, request))


@login_required
def schedule(request):
    template = loader.get_template('schedule.html')
    user = CustomUser.objects.get(username=request.user.username)
    events_no = range(1, len(user.schedule.scheduled_events()) + 1)
    context = {
        'schedule': user.schedule,
        'indexes': events_no,
    }
    if request.method == "POST":
        travelType = request.POST.get('travel', '')
        entry_id = request.POST.get('entry_id', '')
        update_entry = ScheduleEntry.find_by_id(entry_id)
        if request.POST.get('timeschanged', '') == "1":
            if request.POST.get('new_start_time', '') != '':
                update_entry.start = date(request.POST.get('new_start_time', ''))
            if request.POST.get('new_end_time', '') != '':
                update_entry.end = date(request.POST.get('new_end_time', ''))
        update_entry.travelType = travelType
        update_entry.save()
    return HttpResponse(template.render(context, request))


def event(request, id):
    event = Event.find_by_id(int(id))
    tags = event.eventTags.all()
    clashes = request.GET.get('clash')
    if clashes:
        clashes = ScheduleEntry.find_by_id(int(clashes)).event
    inconsistentTime = request.GET.get('inconsistentTime')

    template = loader.get_template('event.html')
    # Will need to split out the veent part of the search template so that we don't get "clashes" appearing everywhere
    if request.user.is_anonymous():
        scheduled_events = []
        username = ""
    else:
        username = request.user.username
        user = CustomUser.objects.get(username=username)
        scheduled_events = user.schedule.scheduled_events()
    if event.recurrence > 0:
        sameGroup = []
        g = event.group
        for e in Event.objects.filter(group=g):
            # if e.group == g:
            if e != event:
                sameGroup.append(e)
    else:
        sameGroup = []
    length = len(sameGroup)
    numTags = len(event.eventTags.all())
    context = {
        'event': event,
        'clashes': clashes,
        'tags': tags,
        'inconsistentTime': inconsistentTime,
        'scheduled_events': scheduled_events,
        'username': username,
        'tickets': event.max_tickets - event.sold_tickets,
        'sameGroup': sameGroup,
        'length': length,
        'numTags': numTags
    }
    return HttpResponse(template.render(context, request))


@login_required
def addEvent(request):
    if request.method == "POST":
        # TODO: check fields
        title = request.POST.get('title', '')
        location = request.POST.get('location', '')
        description = request.POST.get('description', '')
        start_time = date(request.POST.get('startdate', ''))
        end_time = date(request.POST.get('enddate', ''))
        currentUsername = request.user.username
        user = CustomUser.objects.get(username=currentUsername)
        tags = request.POST.getlist('tags[]', [])
        public = request.POST.get('public', '')
        recurrence = int(request.POST.get('recurrence', ''))
        times = int(request.POST.get('times', ''))
        cost = 0
        if recurrence > 0:
            g = GroupOfEvents(title=title)
            g.save()
            for n in range(0, times):
                e = Event(
                        title=title,
                        start_time=start_time,
                        end_time=end_time,
                        location=location,
                        description=description,
                        price=cost,
                        user=user,
                        recurrence=recurrence,
                        group=g
                )
                e.save()
                for tag in tags:
                    e.eventTags.add(tag)
                start_time = start_time + timedelta(days=recurrence)
                end_time = end_time + timedelta(days=recurrence)
        else:
            e = Event(title=title, start_time=start_time, end_time=end_time, location=location, description=description, price=cost, user=user)
            e.save()
            for tag in tags:
                e.eventTags.add(tag)
        if public == "True":
            return redirect("pay", e.id)
        else:
            return redirect('event', e.id)
    else:
        tags = Tag.objects.all()
        template = loader.get_template('addevent.html')
        context = RequestContext(request, {
            'tags': tags
        })
        return HttpResponse(template.render(context, request))


@login_required
def schedule_event(request):
    user = CustomUser.objects.get(username=request.user.username)
    if request.method == "POST":
        if request.POST.get('schedule') == '1':
            try:
                event_id = int(request.POST.get('event_id'))
                event = Event.find_by_id(event_id)
                start_input = request.POST.get('new_start_time', '')
                if start_input == '':
                    new_start_time = event.start_time
                else:
                    new_start_time = date(start_input)
                end_input = request.POST.get('new_end_time', '')
                if end_input == '':
                    new_end_time = event.end_time
                else:
                    new_end_time = date(end_input)
                currentUsername = request.user.username
                user = CustomUser.objects.get(username=currentUsername)
                newentry = ScheduleEntry(
                    event=event,
                    schedule=user.schedule,
                    start=new_start_time,
                    end=new_end_time,
                )
                user.schedule.add_event(newentry)
                return redirect('schedule')
            except EventsClash as e:
                return redirect(reverse('event', args=[event_id]) + '?clash={}'.format(e.e2.id))  # hack
            except InconsistentTime as e:
                return redirect(reverse('event', args=[event_id]) + '?inconsistentTime={}'.format(e.e2))
        else:
            entry_id = int(request.POST.get('entry_id'))
            entry = ScheduleEntry.find_by_id(entry_id)
            user.schedule.remove_event(entry)
            return redirect('schedule')
    else:
        raise Http404("Page not found")


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = CustomUser.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'],
                payment='none',
            )
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect('home')
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
        return render(request, 'index.html')
    elif request.user.is_authenticated():
        return render(request, 'logout.html')
    else:
        return redirect(login)


@login_required()
def accounts(request, username=None):
    currentUsername = request.user.username
    currentUser = CustomUser.objects.get(username=currentUsername)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['docfile']:
                currentUser.profilePicture = form.cleaned_data['docfile']
                currentUser.save()
            else:
                messages.error(request, "Error")
        return HttpResponseRedirect('/accounts/' + currentUsername)
    else:
        events = Event.objects.filter(user=currentUser).order_by('publication_date')
        form = DocumentForm()
        context = {
            'user': currentUser,
            'events': events,
            'form': form
        }
        context.update(get_social_context(currentUser))
        return render_to_response(
            'accounts.html',
            context,
            context_instance=RequestContext(request)
        )


@login_required()
def editAccount(request):
    currentUsername = request.user.username
    currentUser = CustomUser.objects.get(username=currentUsername)
    tags = currentUser.userInterests.all()
    context = {
        'user': currentUser,
        'tags': tags
    }
    template = loader.get_template('ajax/profile.html')
    return HttpResponse(template.render(context, request))


@login_required()
def ownedEvents(request):
    currentUsername = request.user.username
    currentUser = CustomUser.objects.get(username=currentUsername)
    events = Event.objects.filter(user=currentUser).order_by('publication_date')
    context = {
        'events': events
    }
    template = loader.get_template('ajax/events.html')
    return HttpResponse(template.render(context, request))


@login_required()
def interests(request):
    if request.method == 'POST':
        currentUsername = request.user.username
        currentUser = CustomUser.objects.get(username=currentUsername)
        # for interest in currentUser.userInterests.all():
        #     currentUser.userInterests.remove(interest)
        currentUser.userInterests.clear()
        tags = request.POST.getlist('tags[]', [])
        for tag in tags:
            currentUser.userInterests.add(tag)
        template = loader.get_template('accounts.html')
        context = {
            'user': currentUser
        }
        return HttpResponse(template.render(context, request))
    else:
        currentUsername = request.user.username
        currentUser = CustomUser.objects.get(username=currentUsername)
        tags = Tag.objects.all()
        # tags = list(set(Tag.objects.all()) - set(currentUser.userInterests.all()))
        context = {
            'tags': tags,
            'user': currentUser
        }
        template = loader.get_template('ajax/interests.html')
        return HttpResponse(template.render(context, request))


@login_required()
def name(request):
    if request.method == 'POST':
        currentUsername = request.user.username
        currentUser = CustomUser.objects.get(username=currentUsername)
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        currentUser.first_name = firstname
        currentUser.last_name = lastname
        currentUser.save()
        template = loader.get_template('accounts.html')
        context = {
            'user': currentUser
        }
        return HttpResponse(template.render(context, request))
    else:
        return render(request, 'ajax/name.html')


@login_required
def email(request):
    if request.method == 'POST':
        currentUsername = request.user.username
        currentUser = CustomUser.objects.get(username=currentUsername)
        email = request.POST.get('email', '')
        currentUser.email = email
        currentUser.save()
        template = loader.get_template('accounts.html')
        context = {
            'user': currentUser
        }
        return HttpResponse(template.render(context, request))
    else:
        return render(request, 'ajax/email.html')


def change_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            name = request.user.username
            form.save()
            update_session_auth_hash(request, form.user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/accounts/' + name)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changeP.html', {
        'form': form
    })


# this sets the paypal email address
def addPayment(request):
    if request.method == 'POST':
        currentUsername = request.user.username
        currentUser = CustomUser.objects.get(username=currentUsername)
        payment = request.POST.get('payment', '')
        currentUser.payment = payment
        currentUser.save()
        template = loader.get_template('accounts.html')
        context = {
            'user': currentUser,
            'username': currentUser.payment
        }
        return HttpResponse(template.render(context, request))
    else:
        return render(request, 'ajax/addPayment.html')


# this is the paypal button information
@login_required
def pay(request, id):
    # this dictionary takes care of the values needed to be processed through paypal
    paypal_dict = {
        "business": "teamalphaau@gmail.com",
        "currency_code": "GBP",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('event', args=[id])),
        "cancel_return": request.build_absolute_uri(reverse('event', args=[id])),
        "item_number": id,
    }
    # through the hidden form data on the event page the type of payment is being processed
    payment = request.POST.get('pay', '')
    event = Event.find_by_id(int(id))
    name = str(request.user.username)

    # paying to boost the range of event is set to different prices
    if payment == "range1":
        paypal_dict["custom"] = "1"
        paypal_dict["amount"] = "1.50"
        paypal_dict["item_name"] = "Increase range of event"
    elif payment == "range2":
        paypal_dict["custom"] = "2"
        paypal_dict["amount"] = "3"
        paypal_dict["item_name"] = "Increase range of event"
    elif payment == "range3":
        paypal_dict["custom"] = "3"
        paypal_dict["amount"] = "5"
        paypal_dict["item_name"] = "Increase range of event"
    elif payment == "public":
        paypal_dict["custom"] = "0"
        paypal_dict["amount"] = "1.00"
        paypal_dict["item_name"] = "make event public"
        # handles ticket purchases
    elif payment == "ticket":
        paypal_dict["custom"] = name
        paypal_dict["amount"] = str(event.price) + "0"
        paypal_dict["item_name"] = "buy ticket for" + " " + str(event.title)
        # takes the payment email address unless the user kept it empty,
        # then it uses the email used to creat the account
        if event.user.payment == "":
            paypal_dict["business"] = event.user.email
        else:
            paypal_dict["business"] = event.user.payment
    else:
        paypal_dict["custom"] = "666"
        paypal_dict["amount"] = "0.00"
        paypal_dict["item_name"] = "Something went wrong, please go back"

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, "event": event, "pay": payment, }
    return render(request, "payment.html", context)


# this methods fires when a payment has been made through paypal
def handlePayment(sender, **kwargs):
    ipn_obj = sender
    eventid = int(ipn_obj.item_number)
    e = Event.find_by_id(eventid)

    # this checks the custom values given through the payment system and applies various functions based on that
    if ipn_obj.custom == "0":
        e.public = True  # set the event to public
        # apply boosters to the event
    elif ipn_obj.custom == "1":
        e.range = 50
    elif ipn_obj.custom == "2":
        e.range = 100
    elif ipn_obj.custom == "3":
        e.range = 250
    elif ipn_obj.custom == "666":  # if something went wrong, do nothing just send a redirect
        return redirect(event, eventid)
    else:  # this custom value needed to be reserved for the username
        e.sold_tickets += 1
        e.save()
        # get user based on the username input passed through paypal
        currentUsername = str(ipn_obj.custom)
        currentUser = CustomUser.objects.get(username=currentUsername)
        # assign a random string with the username from the purchaser to create the ticket code
        string = currentUsername + "-" + get_random_string(length=16)
        t = Ticket(user=currentUser, event=e, code=string)  # save that ticket
        t.save()
        return redirect(event, int(eventid))

    e.save()
    return redirect(event, int(eventid))


# this tells the system which function it should fire when payment is received
valid_ipn_received.connect(handlePayment)


@staff_member_required
def stats(request):
    s = Summary.most_recent(force=True)
    return render(request, 'stats.html', {'summary': s})


# the create ticket page that sets the number and price of the ticket on an event
def createticket(request, id):
    # find event based on url id
    currentEvent = Event.find_by_id(id)
    if request.method == 'POST':
        # get form info and set the required fields
        currentEvent.max_tickets = request.POST.get('number', '')
        currentEvent.price = request.POST.get('price', '')
        currentEvent.save()
        return redirect(event, id)
    ticket = Ticket.objects.filter(event=currentEvent)
    return render(request, 'createTickets.html', {'id': id, 'ticket': ticket})


# this is the list of tickets that the user bought and can go into to check each ticket
def ticketlist(request):
    # get the current user
    currentUsername = request.user.username
    currentUser = CustomUser.objects.get(username=currentUsername)
    # get the tickets associated by the user from the db
    tickets = Ticket.objects.filter(user=currentUser)
    context = {'tickets': tickets}
    template = loader.get_template('ajax/ticketlist.html')
    return HttpResponse(template.render(context, request))


# this is the ticket page that leads to the unique tickets for each person
def ticket(request, id):
    # it can only be accessed through post because of security issues, otherwise anyone can access it
    if request.method == 'POST':
        # this just gets the ticket id and loads it from the db and passes it to the HTML
        ticket = Ticket.objects.get(id=id)
        context = {'ticket': ticket}
        template = loader.get_template('ticket.html')
        return HttpResponse(template.render(context, request))
    else:
        return redirect(home)
