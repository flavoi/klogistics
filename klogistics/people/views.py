from datetime import date

from django.http import JsonResponse
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from braces.views import LoginRequiredMixin

from seasons.decorators import open_period_only
from allocations.models import Location, Allocation
from .models import Person

def people_json(request):
    """ Restituisce l'elenco delle persone in formato json. """
    people = Person.objects.all()
    people = [ obj.as_dict() for obj in people ]
    return JsonResponse(people, safe=False)


@method_decorator(open_period_only, name='dispatch')
class PersonView(LoginRequiredMixin, ListView):
    """ Espone la lista di persone. """
    model = Person


@method_decorator(open_period_only, name='dispatch')
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
        """ Preparazione dei filtri. """
        allocations = Allocation.objects.get_today_allocations(today)
        locations = Location.objects.filter(allocation__in=allocations)
        locations = locations.annotate(num_allocations=Count('allocation'))
        context['today'] = today
        context['locations'] = locations
        return context


@method_decorator(open_period_only, name='dispatch')
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
