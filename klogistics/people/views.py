from django.http import JsonResponse

from .models import Person

def people_json(request):
    """ Restituisce l'elenco delle persone in formato json """
    people = Person.objects.all()
    people = [ obj.as_dict() for obj in people ]
    return JsonResponse(people, safe=False)