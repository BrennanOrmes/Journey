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

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'perfumes.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

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
    url(r'^user/(?P<username>\w+)/$','aberdeengo.views.user', name='user'),
    #url(r'^user/','aberdeengo.views.user', name='user'),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/(?P<username>\w+)/$', DetailView.as_view(model=CustomUser)),
)