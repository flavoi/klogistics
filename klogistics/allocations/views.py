#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, StringIO, xlsxwriter
from datetime import date, timedelta, datetime

from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.forms import modelformset_factory


from braces.views import LoginRequiredMixin
from extra_views import InlineFormSet, CreateWithInlinesView, ModelFormSetView

from people.models import Person
from seasons.decorators import open_period_only
from seasons.models import Season
from .models import Location, Allocation
from .forms import AllocationForm, AllocationPlainForm


@open_period_only
def manage_allocations(request):
    """ Renderizza il formset di compilazioni della logistica """
    AllocationFormSet = modelformset_factory(
        Allocation, 
        form=AllocationPlainForm,
    )
    if request.method == 'POST':
        formset = AllocationFormSet(request.POST, request.FILES, form_kwargs={'user': request.user})
        if formset.is_valid() and formset:
            formset.save()
            messages.success(request, "Registrazione completata!")
            return redirect('allocations:open_season')
    else:
        formset = AllocationFormSet(
            form_kwargs={'user': request.user},
            queryset=Allocation.objects.none(),
        )
    context = {
        'formset': formset,
    }
    template_name = 'allocations/allocation_create_formset.html'
    return render(request, template_name, context)


@open_period_only
def allocation_season_excel(request, season):
    """ Restituisce le allocazioni della stagione in formato excel """
    
    season = get_object_or_404(Season, pk=season)
    start_date, end_date = season.start_date, season.end_date
    allocations = Allocation.objects.get_season_allocations(start_date, end_date)
    people = Person.objects.all()

    # Inizializza il foglio excel
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet(season.name)
    title_format = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter',
    })
    header_format = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1,
    })

    # Compila titolo del foglio e dati
    title_text = u"{0} {1}".format(ugettext("Logistica"), season.name)
    worksheet_s.merge_range('B2:H2', title_text, title_format)
    for idx, p in enumerate(people):
        worksheet_s.write(4, idx+1, p.surname, header_format)
    delta = end_date - start_date
    for i in range(delta.days + 1):
        row = 5 + i
        current_date = start_date + timedelta(days=i)
        worksheet_s.write(row, 0, current_date.strftime("%d/%m/%Y"))
        for idx, p in enumerate(people):
            today_p_allocation = allocations.filter(person=p)
            today_p_allocation = today_p_allocation.filter(start_date__lte=current_date)
            today_p_allocation = today_p_allocation.filter(end_date__gte=current_date)
            if today_p_allocation:
                # Scrive la prima allocazione del giorno "current_date" per la persona "p"
                worksheet_s.write(row, idx+1, str(today_p_allocation[0].location))
    workbook.close()
    xlsx_data = output.getvalue()
    response.write(xlsx_data)
    return response


@open_period_only
def allocation_season_json(request, season):
    """ Restituisce le allocazioni della stagione in formato json """
    season = get_object_or_404(Season, pk=season)
    start_date, end_date = season.start_date, season.end_date
    allocations = Allocation.objects.get_season_allocations(start_date, end_date)

    # Partiziona i risultati tra quelli dell'utente autenticato e il resto
    all_user = allocations.filter(person__user=request.user)
    all_others = allocations.exclude(person__user=request.user)
    
    if season.is_open():
        # Con stagione aperta solo i risultati utente sono modificabili
        all_user = [obj.as_dict_with_url() for obj in all_user]
    else:
        all_user = [obj.as_dict() for obj in all_user]

    if request.user.is_superuser:
        all_others = [obj.as_dict_with_url() for obj in all_others] 
    else:
        all_others = [obj.as_dict() for obj in all_others] 

    # Concatena i risultati
    allocations_list = all_user + all_others

    # Aggiusta la data fine per includere l'estremo destro nel calendario
    for a in allocations_list:
        inclusive_end_date = datetime.strptime(a['end'], '%Y-%m-%d')
        inclusive_end_date += timedelta(1)
        a['end'] = inclusive_end_date.strftime('%Y-%m-%d')

    return JsonResponse(allocations_list, safe=False)


class AllocationView(LoginRequiredMixin, ListView):
    """ Espone la lista di allocazioni. """
    model = Allocation
    template_name = 'allocations/calendar.html'


class SeasonAllocationView(AllocationView):
    """ Visualizza il calendario relativo alla stagione imputata."""

    def get_queryset(self):
        self.season = Season.objects.get(slug=self.kwargs['slug'])
        self.people = Person.objects.all()
        start_date, end_date = self.season.start_date, self.season.end_date
        return Allocation.objects.get_season_allocations(start_date, end_date)

    def get_context_data(self, **kwargs):
        context = super(SeasonAllocationView, self).get_context_data(**kwargs)
        context['now'] = date.today().strftime("%Y-%m-%d")
        context['season'] = self.season
        context['locations'] = Location.objects.all()
        delta = self.season.end_date - self.season.start_date
        context['season_duration'] = delta.days + 1
        return context


class OpenSeasonAllocationView(SeasonAllocationView):
    """ Visualizza il calendario relativo alla stagione imputata."""
    
    def get_queryset(self):
        self.season = Season.objects.get_open_season()
        self.people = Person.objects.all()
        start_date, end_date = self.season.start_date, self.season.end_date
        return Allocation.objects.get_season_allocations(start_date, end_date)


class AllocationActionMixin(object):
    """ Classe di base per la gestione delle allocazioni """

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
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


@method_decorator(open_period_only, name='dispatch')
class AllocationDetailView(LoginRequiredMixin, DetailView):
    """ Verifica la corretta creazione o modifica delle allocazioni. """
    model = Allocation


@method_decorator(open_period_only, name='dispatch')
class LocationView(LoginRequiredMixin, ListView):
    """ Restituisce la lista dei luoghi censiti a sistema. """
    model = Location
    context_object_name = 'locations'
