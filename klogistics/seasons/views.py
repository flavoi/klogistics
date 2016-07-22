from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Season

@login_required
def park_here(request):
    try:
        season = Season.objects.get_open_season()
    except Season.DoesNotExist:
        template = 'seasons/ended_season.html'
        context = {'season': Season.objects.latest('end_date')}
    else:
        return HttpResponseRedirect(reverse('today'))
    return render(request, template, context)