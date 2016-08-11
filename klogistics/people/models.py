from __future__ import unicode_literals

from django import template
from django.conf import settings
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class PersonManager(models.QuerySet):

    # Estrae tutte le allocazioni, raggruppate per persona, in un determinato giorno
    def get_people_allocations(self, day='2016-08-10'):
        people = self.all().allocation_set.get_today_allocations(day)
        return people


class Person(models.Model):
    """ La singola risorsa del gruppo di lavoro. """
    surname = models.CharField(max_length=30)
    RANK_CHOICES = (
        (u'1', u'stagista'),
        (u'2', u'consultant'),
        (u'3', u'senior'),
        (u'4', u'assistant manager'),
        (u'5', u'manager'),
        (u'6', u'partner'),
    )
    rank = models.CharField(max_length=30, choices=RANK_CHOICES)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    mobile_phone = PhoneNumberField(blank=True)
    office = models.CharField(max_length=30)
    avatar = models.URLField()
    
    def __str__(self):              # __unicode__ on Python 2
        return self.surname

    class Meta:
        ordering = ['surname']
        verbose_name_plural = 'people'

    def as_dict(self): # integration with fullcalendar
        return {
            'id': self.id,
            'title': self.surname + ' ' + self.user.name,
        }
        

class Team(models.Model):
    """ Il gruppo di lavoro. """
    name = models.CharField(max_length=30)
    description = models.TextField()
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):              # __unicode__ on Python 2
        return self.nome


class Membership(models.Model):
    """ Attributi aggiutivi per i membri. """
    member = models.ForeignKey(Person, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    ingress_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=30)
    
    def __str__(self):              # __unicode__ on Python 2
        return self.role
