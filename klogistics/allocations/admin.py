from django.contrib import admin

from .models import Project, Allocation


class AllocationInline(admin.TabularInline):
    model = Project.people.through
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        AllocationInline,
    ]
    exclude = ('people',)