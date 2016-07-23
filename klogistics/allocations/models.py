from __future__ import unicode_literals

import datetime

from django.db import models

from people.models import Person


class AllocationManager(models.QuerySet):
    
    # Estrae tutte le allocazioni, per tutte le risorse, in un determinato periodo
    def get_season_allocations(self, start_date, end_date):
        allocations = self.filter(day__range=[start_date, end_date])
        return allocations

    def get_today_allocations(self, today):
        allocations = self.filter(day=today)
        return allocations


class Location(models.Model):
    """ Luogo nel quale sono allocate i membri del gruppo. """
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    abbreviation = models.CharField(max_length=1, unique=True)
    people = models.ManyToManyField(Person, through='Allocation')

    def __str__(self):              # __unicode__ on Python 2
        return self.name


class Allocation(models.Model):
    """ Schedulazione giornaliera della risorsa. """
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    day = models.DateField()
    comment = models.TextField(blank=True)

    def __str__(self):              # __unicode__ on Python 2
        return "%s-%s-%s" % (str(self.day), self.person, self.location)

    objects = AllocationManager.as_manager()