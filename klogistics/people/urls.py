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
]