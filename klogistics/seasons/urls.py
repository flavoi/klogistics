from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^fine-stagione/$', view=views.park_here, name='fine_stagione'),
]