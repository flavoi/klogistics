import datetime
from datetime import datetime, date, timedelta as td
from random import randint

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
        start_date = season.start_date.toordinal()
        end_date = season.end_date.toordinal()
        for p in people:
            allocation_times = randint(2,4)
            for i in range(1, allocation_times, 1):
                random_location = Location.objects.all().order_by('?')[0]
                random_start_date = date.fromordinal(randint(start_date, end_date))
                random_end_date = random_start_date + td(days=randint(1,4))
                allocation = Allocation(
                    location = random_location, 
                    person=p, 
                    start_date=random_start_date,
                    end_date=random_end_date,
                )
                allocation.save()
                print "Allocazione creata %s" % allocation