import datetime
from datetime import datetime, date, timedelta as td

from django.core.management.base import BaseCommand

from allocations.models import Allocation, Location
from people.models import Person
from seasons.models import Season


class Command(BaseCommand):
    """ Popola con allocazioni casuali una certa data del tipo aaaa-mm-gg"""
    help = 'Fill random allocations in a given date span.'
    
    def add_arguments(self, parser):    
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete poll instead of closing it',
        )

    def handle(self, *args, **options):
        people = Person.objects.all()
        print "Pulisco allocazioni correnti."
        Allocation.objects.all().delete()
        print "Allocazioni cancellate."
        if options['delete']:
            return
        season = Season.objects.get_open_season()
        delta = season.end_date - season.start_date
        day_range = [season.start_date + td(days=day) for day in range(delta.days + 1)]
        for p in people:
            for day in day_range:
                random_location = Location.objects.all().order_by('?')[0]
                allocation = Allocation(location = random_location, person=p, day=day)
                allocation.save()
                print "Allocazione creata %s" % allocation