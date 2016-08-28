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

    def __str__(self):              # __unicode__ on Python 2
        return u'%s %s' % (self.slug, self.end_date)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Season, self).save(*args, **kwargs)

    
    def is_open(self):              # Controlla se la stagione e` valida e aperta
        if self.state == '1' and self.available:
            return True
        return False

    objects = SeasonManager.as_manager()