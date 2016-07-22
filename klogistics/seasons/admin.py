from django.contrib import admin

from .models import Season


@admin.register(Season)
class StagioneAdmin(admin.ModelAdmin):
    list_display = ('end_date', 'start_date', 'state')