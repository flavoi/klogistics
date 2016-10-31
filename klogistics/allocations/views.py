import json
from datetime import date, timedelta, datetime

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy

from braces.views import LoginRequiredMixin

from people.models import Person
from seasons.decorators import open_period_only
from seasons.models import Season
from .models import Location, Allocation
from .forms import AllocationForm


def allocation_season_json(request, season):
    """ Restituisce le allocazioni della stagione in formato json """
    season = get_object_or_404(Season, pk=season)
    start_date, end_date = season.start_date, season.end_date
    allocations = Allocation.objects.get_season_allocations(start_date, end_date)

    # Partiziono i risultati tra quelli dell'utente autenticato e il resto
    all_user = allocations.filter(person__user=request.user)
    all_others = allocations.exclude(person__user=request.user)
    
    if season.is_open():
        # Con stagione aperta solo i risultati utente sono modificabili 
        all_user = [obj.as_dict_with_url() for obj in all_user]
    else:
        all_user = [obj.as_dict() for obj in all_user]

    all_others = [obj.as_dict() for obj in all_others] 

    # Concateno i risultati
    allocations_list = all_user + all_others

    for a in allocations_list:
        virtual_end_date = datetime.strptime(a['end'], '%Y-%m-%d')
        virtual_end_date += timedelta(1)
        a['end'] = virtual_end_date.strftime('%Y-%m-%d')

    return JsonResponse(allocations_list, safe=False)


class AllocationView(LoginRequiredMixin, ListView):
    """ Espone la lista di allocazioni. """
    model = Allocation


class SeasonAllocationView(AllocationView):
    """ Visualizza il calendario relativo alla Stagione imputata."""

    def get_queryset(self):
        self.season = Season.objects.get(slug=self.kwargs['slug'])
        # self.season = Season.objects.all()[0]
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

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        return super(AllocationActionMixin, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AllocationActionMixin, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(open_period_only, name='dispatch')
class AllocationCreateView(LoginRequiredMixin, AllocationActionMixin, CreateView):
    """ Gestisce la creazione delle allocazioni. """
    model = Allocation
    template_name_suffix = '_create'
    success_msg = "Registrazione completata!"
    form_class = AllocationForm


@method_decorator(open_period_only, name='dispatch')
class AllocationUpdateView(LoginRequiredMixin, AllocationActionMixin, UpdateView):
    """ Gestisce la modifica delle allocazioni. """
    model = Allocation
    template_name_suffix = '_update'
    success_msg = "Logistica modificata!"
    form_class = AllocationForm


@method_decorator(open_period_only, name='dispatch')
class AllocationDeleteView(LoginRequiredMixin, AllocationActionMixin, DeleteView):
    """ Gestisce la cancellazione delle allocazioni. """
    model = Allocation
    success_msg = "Logistica cancellata!"
    
    def get_success_url(self, **kwargs):
        season = Season.objects.get_open_season()
        return reverse_lazy('allocations:season', kwargs={'slug':season.slug})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super(AllocationDeleteView, self).delete(request, *args, **kwargs)


class AllocationDetailView(LoginRequiredMixin, DetailView):
    """ Verifica la corretta creazione o modifica delle allocazioni. """
    model = Allocation


class LocationView(LoginRequiredMixin, ListView):
    """ Restituisce la lista dei luoghi censiti a sistema. """
    model = Location
    context_object_name = 'locations'
