from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'pad', 'created_by', 'start', 'end', 'private', 'active')
    list_filter = ('private', 'active')
    readonly_fields = ('slug',)
