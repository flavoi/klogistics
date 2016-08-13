import json
from datetime import date

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib import messages

from braces.views import LoginRequiredMixin

from people.models import Person
from seasons.decorators import open_period_only
from seasons.models import Season
from .models import Location, Allocation


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
    """ Espone la lista di allocazioni. """
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


class AllocationActionMixin(object):
    """ Classe di base per la gestione delle allocazioni """
    fields = ('location', 'person', 'start_date', 'end_date')

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(AllocationActionMixin, self).form_valid(form)


class AllocationCreateView(LoginRequiredMixin, AllocationActionMixin, CreateView):
    """ Gestisce la creazione delle allocazioni. """
    model = Allocation
    template_name_suffix = '_create'
    success_msg = "Registrazione completata!"


class AllocationUpdateView(LoginRequiredMixin, AllocationActionMixin, UpdateView):
    """ Gestisce la modifica delle allocazioni. """
    model = Allocation
    template_name_suffix = '_update'
    success_msg = "Logistica modificata!"


class AllocationDetailView(LoginRequiredMixin, DetailView):
    """ Verifica la corretta creazione o modifica delle allocazioni. """
    model = Allocation


class LocationView(LoginRequiredMixin, ListView):
    """ Restituisce la lista dei luoghi censiti a sistema. """
    model = Location
    context_object_name = 'locations'
