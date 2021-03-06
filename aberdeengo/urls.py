"""
    urls.py - URL configuration.

    Author: Team Alpha

    Tested?: Yes
    Functional?: Yes
    Merged?: Yes
    Copyright: (c) 2016, 2017 Team Alpha, University of Aberdeen.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf import settings
from django.conf.urls import url, patterns, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.detail import DetailView

from haystack.views import SearchView

from models import CustomUser

import aberdeengo.views


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', aberdeengo.views.home, name='home'),
    url(r'^$', aberdeengo.views.home, name='home'),
    url(r'^search/$', SearchView(), name='search'),  # TODO: don't hardcode results_per_page=5
    url(r'^contact/$', aberdeengo.views.contact, name='contact'),
    url(r'^schedule/$', aberdeengo.views.schedule, name='schedule'),
    url(r'^event/([0-9]+)$', aberdeengo.views.event, name='event'),  # TODO: change urls to event/eventname+number
    url(r'^addevent/', aberdeengo.views.addEvent, name='addevent'),
    url(r'^scheduleevent/', aberdeengo.views.schedule_event, name='scheduleevent'),
    url(r'^signup/', aberdeengo.views.signup, name='signup'),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/$', aberdeengo.views.accounts, name='accounts'),
    url(r'^accounts/(?P<username>\w+)/$', aberdeengo.views.accounts, name='accounts'),
    url(r'^editAccount/$', aberdeengo.views.editAccount, name='editAccount'),
    url(r'^interests/$', aberdeengo.views.interests, name='interests'),
    url(r'^ownedEvents/$', aberdeengo.views.ownedEvents, name='ownedEvents'),
    url(r'^name/$', aberdeengo.views.name, name='name'),
    url(r'^email/$', aberdeengo.views.email, name='email'),
    url(r'^password/$', aberdeengo.views.change_password, name='change_password'),
    url(r'^addPayment/$', aberdeengo.views.addPayment, name='addPayment'),
    url(r'^pay/([0-9]+)$', aberdeengo.views.pay, name='pay'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^stats/$', aberdeengo.views.stats, name='stats'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^createticket/([0-9]+)$', aberdeengo.views.createticket, name='createticket'),
    url(r'^ticketlist/$', aberdeengo.views.ticketlist, name='ticketlist'),
    url(r'^ticket/([0-9]+)$', aberdeengo.views.ticket, name='ticket'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
    url(r'^static/(?P<path>.*)$', views.serve),
]
