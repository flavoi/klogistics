from __future__ import unicode_literals
import datetime

from django.db import models
from django.core.urlresolvers import reverse

from people.models import Person

from colorfield.fields import ColorField


class AllocationManager(models.QuerySet):
    
    # Estrae tutte le allocazioni, per tutte le persone, in un determinato periodo
    def get_season_allocations(self, start_date, end_date):
        allocations = self.filter(start_date__range=[start_date, end_date])
        return allocations

    # Estrae tutte le allocazioni, per tutte le persone, in un determinato giorno
    def get_today_allocations(self, today):
        allocations = self.filter(start_date__lte=today).filter(end_date__gte=today)
        return allocations


class Location(models.Model):
    """ Luogo nel quale sono allocate i membri del gruppo. """
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    color = ColorField(default='#FF0000')
    people = models.ManyToManyField(Person, through='Allocation', related_name='people')

    def __str__(self):              # __unicode__ on Python 2
        return self.name


class Allocation(models.Model):
    """ Schedulazione giornaliera della risorsa. """
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name='luogo')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='persona')
    start_date = models.DateField(verbose_name='data inizio')
    end_date = models.DateField(verbose_name='data fine')
    comment = models.TextField(blank=True, verbose_name='commento')

    def __str__(self):              # __unicode__ on Python 2
        return "%s-%s-%s-%s" % (str(self.start_date), str(self.end_date), self.person, self.location)

    def as_dict(self): # integrazione con fullcalendar
        return {
            'id': str(self.id),
            'resourceId': str(self.person.pk),
            'start': self.start_date.strftime("%Y-%m-%d"),
            'end': self.end_date.strftime("%Y-%m-%d"),
            'title': self.location.name,
            'color': self.location.color,
        }

    def as_dict_with_url(self): # integrazione con fullcalendar con url
        d = self.as_dict()
        url_d = {'url': reverse("allocations:update", kwargs={"pk": self.pk})}
        d.update(url_d)
        return d

    objects = AllocationManager.as_manager()

    def get_absolute_url(self):
        return reverse("allocations:detail", kwargs={"pk": self.pk})