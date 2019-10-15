from django.contrib import admin
from .models import AppUser


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'id',
        'username',
        'password',
    )
    readonly_fields = ('id',)
