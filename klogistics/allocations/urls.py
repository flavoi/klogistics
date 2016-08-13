from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^stagione/([0-9]+)/$', 
        view=views.SeasonAllocationView.as_view(), 
        name='season'),
    url(r'^stagione-json/([0-9]+)/$',
        view=views.allocation_season_json,
        name='season-json'),
    url(r'^luoghi/$',
        view=views.LocationView.as_view(),
        name='locations'),
    url(r'^registrazione/$',
        view=views.AllocationCreateView.as_view(),
        name='create'),
    url(r'^modifica/(?P<pk>\d+)/$',
        view=views.AllocationUpdateView.as_view(),
        name='update'),
    url(r'^verifica/(?P<pk>\d+)/$',
        view=views.AllocationDetailView.as_view(),
        name='detail'),
]