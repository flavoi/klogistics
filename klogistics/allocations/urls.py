from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', 
        view=views.OpenSeasonAllocationView.as_view(), 
        name='open_season'),
    url(r'^periodo/(?P<slug>[\w-]+)/$', 
        view=views.SeasonAllocationView.as_view(), 
        name='season'),
    url(r'^periodo-json/(?P<season>\d+)/$',
        view=views.allocation_season_json,
        name='season-json'),
    url(r'^luoghi/$',
        view=views.LocationView.as_view(),
        name='locations'),
    url(r'^registrazione/$',
        view=views.AllocationCreateView.as_view(),
        name='create'),
    url(r'^registrazione/multipla/$', 
        view=views.manage_allocations,
        name='create-set'),
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