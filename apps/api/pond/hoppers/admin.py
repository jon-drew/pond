from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Hopper, Pair, RefreshToken


@admin.register(Hopper)
class HopperAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'anonymous', 'slug', 'created_at')
    list_filter = ('anonymous',)
    fieldsets = UserAdmin.fieldsets + (
        ('Pond', {'fields': ('name', 'birth_date', 'anonymous', 'slug')}),
    )


@admin.register(Pair)
class PairAdmin(admin.ModelAdmin):
    list_display = ('first_hopper', 'second_hopper')


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ('hopper', 'expires_at', 'created_at')
    readonly_fields = ('token',)
