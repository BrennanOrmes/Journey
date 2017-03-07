"""aberdeengo URL Configuration

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
from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.views.generic.detail import DetailView
from models import CustomUser
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',


    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','aberdeengo.views.home', name='home'),
    url(r'^home/$','aberdeengo.views.home', name='home'),
    url(r'^search/$','aberdeengo.views.searchEvents', name='search'),
    url(r'^contact/$','aberdeengo.views.contact', name='contact'),
    url(r'^schedule/$','aberdeengo.views.schedule', name='schedule'),
    url(r'^event/([0-9]+)$','aberdeengo.views.event', name='event'), #TODO: change urls to event/eventname+number
    url(r'^addevent/','aberdeengo.views.addEvent', name='addevent'),
    url(r'^scheduleevent/','aberdeengo.views.schedule_event', name='scheduleevent'),
    url(r'^signup/','aberdeengo.views.signup', name='signup'),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/(?P<username>\w+)/$','aberdeengo.views.accounts', name='accounts'),
    url(r'^editAccount/$','aberdeengo.views.editAccount', name='editAccount'),
    url(r'^interests/$','aberdeengo.views.interests', name='interests'),
    url(r'^ownedEvents/$','aberdeengo.views.ownedEvents', name='ownedEvents'),
    url(r'^name/$','aberdeengo.views.name', name='name'),
    url(r'^email/$','aberdeengo.views.email', name='email'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^addPayment/$', 'aberdeengo.views.addPayment', name='addPayment'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.conf import settings
from django.contrib.staticfiles import views

urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
    url(r'^static/(?P<path>.*)$', views.serve),
]