from datetime import date, datetime, timedelta

from django.http import JsonResponse
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from braces.views import LoginRequiredMixin

from seasons.decorators import open_period_only
from allocations.models import Location, Allocation
from .models import Person, Membership, Team


def teams_json(request):
    """ Restituisce l'elenco delle squadre in formato json. """
    teams = Team.objects.all()
    teams = [ obj.as_dict() for obj in teams ]
    return JsonResponse(teams, safe=False)


def search_day_allocation(request):
    """ Ricerca la logistica del giorno specificato. """
    date = request.GET.get('q')
    try:
        date = datetime.strptime(date, '%d/%m/%Y').date()
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
    return HttpResponseRedirect(reverse('people:day', args=(year,month,day,)))


class PersonView(LoginRequiredMixin, ListView):
    """ Espone la lista di persone. """
    model = Person


class TodayPersonView(PersonView):
    """ Espone la logistica di oggi. """
    template_name = 'people/person_list.html'
    context_object_name = 'people'

    def get_today(self):
        today = date.today()
        return today

    def get_queryset(self):
        today = self.get_today()
        people = Person.objects.all()
        return people

    def get_context_data(self, **kwargs):
        context = super(TodayPersonView, self).get_context_data(**kwargs)
        today = self.get_today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        """ Preparazione dei filtri. """
        allocations = Allocation.objects.get_today_allocations(today)
        locations = Location.objects.filter(allocation__in=allocations)
        locations = locations.annotate(num_allocations=Count('allocation'))
        context['today'] = today
        context['tomorrow'] = tomorrow
        context['yesterday'] = yesterday
        context['locations'] = locations
        return context


class DayPersonView(TodayPersonView):
    """ Espone la logistica del giorno specificato. """

    def get_today(self):
        year = int(self.args[0])
        month = int(self.args[1])
        day = int(self.args[2])
        today = date(year, month, day)
        return today


class LocationDayPersonView(DayPersonView):
    """ Filtra la logistica del giorno per uno specifico luogo. """

    def get_queryset(self):
        queryset = super(LocationDayPersonView, self).get_queryset()
        location = self.args[3]
        allocations = Allocation.objects.get_today_allocations(self.get_today())
        allocations = allocations.filter(location__name = location)
        people = queryset.filter(allocation__in = allocations)
        return people

    def get_context_data(self, **kwargs):
        context = super(LocationDayPersonView, self).get_context_data(**kwargs)
        context['nav_active'] = self.args[3]
        return context
