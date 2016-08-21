from __future__ import unicode_literals
import datetime

from django.db import models
from django.core.urlresolvers import reverse

from people.models import Person


class AllocationManager(models.QuerySet):
    
    # Estrae tutte le allocazioni, per tutte le risorse, in un determinato periodo
    def get_season_allocations(self, start_date, end_date):
        allocations = self.filter(start_date__range=[start_date, end_date])
        return allocations

    # Estrae tutte le allocazioni, per tutte le risorse, in un determinato giorno
    def get_today_allocations(self, today):
        allocations = self.filter(start_date__lte=today).filter(end_date__gt=today)
        return allocations


class Location(models.Model):
    """ Luogo nel quale sono allocate i membri del gruppo. """
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    COLOR_CHOICES = (
        (u'green', u'verde'),
        (u'orange', u'arancio'),
        (u'red', u'rosso'),
        (u'#3a87ad', u'azzurro'),
        (u'hotpink', u'rosa'),
    )
    color = models.CharField(max_length=30, choices=COLOR_CHOICES, default='azure')
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

    objects = AllocationManager.as_manager()

    def get_absolute_url(self):
        return reverse("allocations:detail", kwargs={"pk": self.pk})