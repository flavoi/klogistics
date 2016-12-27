from django.conf.urls import url
from django.contrib.auth.views import login as djlogin
from django.contrib.auth.views import logout as djlogout
from django.contrib.auth.views import password_change as djpwchange

from . import views

urlpatterns = [
    url(r'^login/$', view=djlogin, name='login'),
    url(r'^logout/$', view=djlogout, name='logout'),
    url(r'^cambio-password/$', view=djpwchange, name='pwchange'),
    url(r'^squadre-json/$', view=views.teams_json, name='teamsjson'),
    url(r'^$',
        view=views.TodayPersonView.as_view(),
        name='today'),
    url(r'^([0-9]{4})/([0-9]{2})/([0-9]+)/$',
        view=views.DayPersonView.as_view(),
        name='day'),
    url(r'^([0-9]{4})/([0-9]{2})/([0-9]+)/([-\w\d]+)/$',
        view=views.LocationDayPersonView.as_view(),
        name='location-day'),
    url(r'^ricerca/$',
        view=views.search_day_allocation,
        name='search_day_allocation'),
]