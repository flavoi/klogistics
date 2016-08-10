from django import template

register = template.Library()

@register.filter
def people_allocation_day(allocation, day):
    """
        Filtra la lista di allocazioni della persona per le sole 
        allocazioni del giorno.
    """
    return allocation.get_today_allocations(day)