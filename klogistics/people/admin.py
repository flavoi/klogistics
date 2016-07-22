from django.contrib import admin

from .models import Team, Person


class MembershipInline(admin.TabularInline):
    model = Team.members.through
    extra = 1

@admin.register(Person)
class PersonAdimin(admin.ModelAdmin):
    list_display = ('surname', 'user', 'rank')
    model = Person

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]
    exclude = ('members',)