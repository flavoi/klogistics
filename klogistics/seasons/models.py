from django.db import models
from django.utils import timezone


class SeasonManager(models.QuerySet):
    
    # Estrae la stagione valida
    def get_open_season(self):
        season = self.get(state='1')
        return season


class Season(models.Model):
    """ Attiva la funzionalita` qualora stato sia impostato a vero. """
    STATES = (
        ('0', 'chiusa'),
        ('1', 'aperta'),
    )
    start_date = models.DateField()
    end_date = models.DateField()
    state = models.CharField(max_length=6, choices=STATES)

    def __str__(self):              # __unicode__ on Python 2
        return u'%s' % (self.end_date)
    
    objects = SeasonManager.as_manager()