from datetime import date, timedelta as td

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.decorators import method_decorator
from django.utils import timezone

from braces.views import LoginRequiredMixin

from .models import Location, Allocation
from people.models import Person
from seasons.decorators import open_period_only
from seasons.models import Season

from django.shortcuts import render
from django.utils.safestring import mark_safe
from kcalendar import KCalendar


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
        allocations = self.get_queryset()
        season = self.season
        people = self.people
        # Estrae tutti i giorni della stagione corrente
        delta = season.end_date - season.start_date
        days = [season.start_date + td(days=day) for day in range(delta.days + 1)]
        calendar = []
        calendar.append({('persone',): days})
        # compila il calendario
        for person in people:
            name_surname = (
                person.user.name,
                person.surname,
            )
            person_allocations = allocations.filter(person=person)
            day_allocations = []
            for day in days:
                try:
                    today_allocation = person_allocations.filter(day=day).values_list(
                        'location__name', 
                        'location__description',
                        'location__abbreviation'
                    )
                except Allocation.DoesNotExist:
                    today_allocation = ''
                day_allocations.append(today_allocation)
            calendar.append({name_surname: [allocation for allocation in day_allocations]})
        context['calendar'] = calendar
        context['season'] = season
        return context


class TodayAllocationView(AllocationView):
    """ Visualizza la logistica del giorno solare. """
    template_name = 'allocations/allocation_today.html'
    context_object_name = 'today_allocations'

    def get_today(self):
        today = date.today()
        return today

    def get_queryset(self):
        today = timezone.now()     
        allocations = Allocation.objects.get_today_allocations(today)
        return allocations

    def get_context_data(self, **kwargs):
        context = super(TodayAllocationView, self).get_context_data(**kwargs)
        today = self.get_today()
        """ Preparazione filtri successivi. """
        locations = Location.objects.all() 
        context['today'] = today
        context['locations'] = locations
        return context


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
        return allocations


class LocationDayAllocationView(DayAllocationView):
    """ Filtra la logistica del giorno per uno specifico luogo. """

    def get_queryset(self):
        today = self.get_today()
        location = self.args[3]
        allocations = Allocation.objects.get_today_allocations(today)
        allocations = allocations.filter(location__name=location)
        return allocations

    def get_context_data(self, **kwargs):
        context = super(LocationDayAllocationView, self).get_context_data(**kwargs)
        context['nav_active'] = self.args[3]
        return context


class LocationView(LoginRequiredMixin, ListView):
    """ Restituisce la lista dei luoghi censiti a sistema. """
    model = Location
    context_object_name = 'locations'