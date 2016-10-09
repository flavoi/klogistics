from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^stagione/(?P<slug>[\w-]+)/$', 
        view=views.SeasonAllocationView.as_view(), 
        name='season'),
    url(r'^stagione-json/(?P<season>\d+)/$',
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
    url(r'^cancella/(?P<pk>\d+)/$',
        view=views.AllocationDeleteView.as_view(),
        name='delete'),
]