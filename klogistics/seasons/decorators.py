"""
    Associabili a viste in tutte le app del progetto.
"""
import datetime
from functools import wraps

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import available_attrs

from .models import Season

# Inibisce la funzionalita` in caso di periodo chiuso
def open_period_only(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapper(request, *args, **kwargs):
        try:
            season = Season.objects.get_open_season()
        except Season.DoesNotExist:
            return HttpResponseRedirect(reverse('fine_stagione'))
        else:
            return view_func(request, *args, **kwargs)
    return wrapper