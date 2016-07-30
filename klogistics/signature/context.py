"""
    Custom context processors for the signature app.
    This script contains useful informations for every template.
"""
from datetime import date

def get_signature(request):
    """ Firma automatica del tipo FM YYYY-YYYY """
    START_YEAR = 2016
    this_year = date.today().year
    if START_YEAR != this_year:
        copy_year = "%s - %s" % (START_YEAR, this_year)
    else:
        copy_year = START_YEAR
    signature = "FM %s" % copy_year
    return { 'signature': signature }