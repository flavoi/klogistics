from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify


class SeasonManager(models.QuerySet):
    
    # Estrae l'elenco delle stagioni disponibili    
    def get_available_seasons(self):
        seasons = self.filter(available=True)
        return seasons

    # Estrae la stagione valida
    def get_open_season(self):
        season = self.get_available_seasons().get(state='1')
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
    available = models.BooleanField(default=True)
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30)
    number = models.PositiveIntegerField(primary_key=True)

    def __str__(self):              # __unicode__ on Python 2
        return u'%s %s' % (self.slug, self.end_date)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.number:
            s = self.name
            n = [int(s) for s in str.split() if s.isdigit()][0]
            number = n
        super(Season, self).save(*args, **kwargs)

    objects = SeasonManager.as_manager()