from django.contrib import admin
from .models import Pad


@admin.register(Pad)
class PadAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'owner', 'active', 'slug', 'created_at')
    list_filter = ('active',)
    readonly_fields = ('slug',)
