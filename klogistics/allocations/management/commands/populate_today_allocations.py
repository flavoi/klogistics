import datetime
from datetime import datetime

from django.core.management.base import BaseCommand

from allocations.models import Allocation, Project
from people.models import Person


class Command(BaseCommand):
    """ Popola con allocazioni casuali una certa data del tipo aaaa-mm-gg"""
    args = '<foo bar ...>'
    help = 'Popola allocazioni casuali in data di oggi'

    def add_arguments(self, parser):
        parser.add_argument('date', nargs='+', type=str)

    def handle(self, *args, **options):
        people = Person.objects.all()
        if options['date']:
            today = datetime.strptime(options['date'][0], '%Y-%m-%d')
        else:
            today = datetime.date.today()
        for p in people:
            random_project = Project.objects.all().order_by('?')[0]
            allocation = Allocation(project = random_project, person=p, day=today)
            allocation.save()
            print "Allocazione creata %s" % allocation