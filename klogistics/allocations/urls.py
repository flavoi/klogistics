from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^stagione/([0-9]+)/$', 
        view=views.SeasonAllocationView.as_view(), 
        name='season'),
    url(r'^$',
        view=views.TodayAllocationView.as_view(),
        name='today'),
    url(r'^([0-9]{4})/([0-9]{2})/([0-9]+)/$',
        view=views.DayAllocationView.as_view(),
        name='day'),
    url(r'^([0-9]{4})/([0-9]{2})/([0-9]+)/([-\w\d]+)/$',
        view=views.LocationDayAllocationView.as_view(),
        name='location-day'),
    url(r'^luoghi/$',
        view=views.LocationView.as_view(),
        name='locations'),
    url(r'^stagione-json/([0-9]+)/$',
        view=views.allocation_season_json,
        name='season-json'),
    url(r'^search-day-allocation/$',
        view=views.search_day_allocation,
        name='search_day_allocation'),
]