from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^logistica/$', 
        view=views.SeasonAllocationView.as_view(), 
        name='season'),
    url(r'^$',
        view=views.TodayAllocationView.as_view(),
        name='today'),
    url(r'^([0-9]{4})/([0-9]{2})/([0-9]+)/$',
        view=views.DayAllocationView.as_view(),
        name='day'),
    url(r'^([0-9]{4})/([0-9]{2})/([0-9]+)/([-\w\d]+)/$',
        view=views.ProjectDayAllocationView.as_view(),
        name='project-day'),
]