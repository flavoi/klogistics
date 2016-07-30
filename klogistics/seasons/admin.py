from django.contrib import admin

from .models import Season


@admin.register(Season)
class StagioneAdmin(admin.ModelAdmin):
    list_display = ('name', 'end_date', 'start_date', 'state', 'available')
    prepopulated_fields = {
        "slug": ("name",),
    }