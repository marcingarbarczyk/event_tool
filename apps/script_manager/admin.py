from django.contrib import admin

from .models import Script, Service


@admin.register(Service)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    search_fields = ('name',)


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'service',
        'script_type',
    )
    search_fields = (
        'service__name',
        'script_type',
    )
    list_filter = ('script_type',)
