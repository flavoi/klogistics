from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^stagione/([0-9]+)/$', 
        view=views.SeasonAllocationView.as_view(), 
        name='season'),
    url(r'^luoghi/$',
        view=views.LocationView.as_view(),
        name='locations'),
    url(r'^stagione-json/([0-9]+)/$',
        view=views.allocation_season_json,
        name='season-json'),
]