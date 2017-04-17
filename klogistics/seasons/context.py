"""
    Custom context processors for the seasons app.
    This script contains useful informations for every template.
"""
from .models import Season

def get_seasons(request):
    """ Restituisce l'elenco delle stagioni disponibili. """
    seasons = Season.objects.get_available_seasons().order_by('-end_date')
    return { 'seasons': seasons }

def get_open_season(request):
    """ Restituisce la stagione aperta. """
    season = Season.objects.get_open_season()
    return { 'season': season }