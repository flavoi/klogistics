from django.contrib import admin

from .models import Location, Allocation


class AllocationInline(admin.TabularInline):
    model = Location.people.through
    extra = 1

@admin.register(Location)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        AllocationInline,
    ]
    exclude = ('people',)