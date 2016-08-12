import json
from datetime import date, datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib import messages

from braces.views import LoginRequiredMixin

from .models import Location, Allocation
from people.models import Person
from seasons.decorators import open_period_only
from seasons.models import Season


@open_period_only
def allocation_season_json(request, season):
    """ Restituisce le allocazioni della stagione in formato json """
    season = get_object_or_404(Season, pk=season)
    start_date, end_date = season.start_date, season.end_date
    allocations = Allocation.objects.get_season_allocations(start_date, end_date)
    allocations = [ obj.as_dict() for obj in allocations ]
    return JsonResponse(allocations, safe=False)


@method_decorator(open_period_only, name='dispatch')
class AllocationView(LoginRequiredMixin, ListView):
    """ Visualizza una specifica allocazione. """
    model = Allocation


@method_decorator(open_period_only, name='dispatch')
class SeasonAllocationView(AllocationView):
    """ Visualizza il calendario relativo alla Stagione imputata."""

    def get_queryset(self):
        self.season = get_object_or_404(Season, pk=self.args[0])
        self.people = Person.objects.all()
        start_date, end_date = self.season.start_date, self.season.end_date
        return Allocation.objects.get_season_allocations(start_date, end_date)

    def get_context_data(self, **kwargs):
        context = super(SeasonAllocationView, self).get_context_data(**kwargs)
        context['now'] = date.today().strftime("%Y-%m-%d")
        context['season'] = self.season
        delta = self.season.end_date - self.season.start_date
        context['season_duration'] = delta.days + 1
        return context


@method_decorator(open_period_only, name='dispatch')
class TodayAllocationView(AllocationView):
    """ Visualizza la logistica del giorno. """
    template_name = 'allocations/allocation_today.html'
    context_object_name = 'people'

    def get_today(self):
        today = date.today()
        return today

    def get_queryset(self):
        today = self.get_today()
        allocations = Allocation.objects.get_today_allocations(today)
        people = Person.objects.filter(allocation__in = allocations)
        return people

    def get_context_data(self, **kwargs):
        context = super(TodayAllocationView, self).get_context_data(**kwargs)
        today = self.get_today()
        """ Preparazione filtri successivi. """
        locations = Location.objects.all() 
        context['today'] = today
        context['locations'] = locations
        return context


@method_decorator(open_period_only, name='dispatch')
class DayAllocationView(TodayAllocationView):
    """ Visualizza la logistica del giorno specificato. """

    def get_today(self):
        year = int(self.args[0])
        month = int(self.args[1])
        day = int(self.args[2])
        today = date(year, month, day)
        return today

    def get_queryset(self):
        today = self.get_today()
        allocations = Allocation.objects.get_today_allocations(today)
        people = Person.objects.filter(allocation__in = allocations)
        return people


class LocationDayAllocationView(DayAllocationView):
    """ Filtra la logistica del giorno per uno specifico luogo. """

    def get_queryset(self):
        today = self.get_today()
        location = self.args[3]
        allocations = Allocation.objects.get_today_allocations(today)
        allocations = allocations.filter(location__name=location)
        people = Person.objects.filter(allocation__in = allocations)
        return people

    def get_context_data(self, **kwargs):
        context = super(LocationDayAllocationView, self).get_context_data(**kwargs)
        context['nav_active'] = self.args[3]
        return context


class LocationView(LoginRequiredMixin, ListView):
    """ Restituisce la lista dei luoghi censiti a sistema. """
    model = Location
    context_object_name = 'locations'


@open_period_only
def search_day_allocation(request):
    date = request.GET.get('q')
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        if date == '':
            message = 'Imposta un criterio di ricerca diverso da vuoto :-)'
            messages.add_message(request, messages.WARNING, message)
        else:
            message = 'Ricerca fallita: assicurati di riportare la data come nella casella.'
            messages.add_message(request, messages.ERROR, message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    return HttpResponseRedirect(reverse('day', args=(year,month,day,)))