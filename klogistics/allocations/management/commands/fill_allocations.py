import datetime
from datetime import datetime, date, timedelta as td
from random import randint

from django.core.management.base import BaseCommand

from allocations.models import Allocation, Location
from people.models import Person
from seasons.models import Season


class Command(BaseCommand):
    """ Popola con allocazioni casuali la stagione aperta """
    help = 'Fill random allocations in the open season.'
    
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
        for p in people: 
            i = 1
            start_date = season.start_date
            random_end_date = season.start_date # Initialization
            random_location = new_random_location = ''
            while(i == 1):
                start_date = random_end_date
                new_random_end_date = random_end_date + td(days=randint(1,20))
                if new_random_end_date > season.end_date:
                    new_random_end_date = season.end_date + td(days=1) # Do not go past season end date
                random_end_date = new_random_end_date
                while new_random_location == random_location:
                    new_random_location = Location.objects.all().order_by('?')[0]
                random_location = new_random_location
                allocation = Allocation(
                    location = random_location, 
                    person=p, 
                    start_date=start_date,
                    end_date=random_end_date,
                )
                allocation.save()
                print "Allocazione creata %s" % allocation
                if random_end_date >= season.end_date:
                    i = 0
