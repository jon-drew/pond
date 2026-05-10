from django.contrib import admin
from .models import Ribbit


@admin.register(Ribbit)
class RibbitAdmin(admin.ModelAdmin):
    list_display = ('sent_by', 'event', 'echo_of', 'slug', 'created_at')
    readonly_fields = ('slug',)
