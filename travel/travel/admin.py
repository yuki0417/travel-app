from django.contrib import admin
from .models import Place, Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'user',
        'name',
        'radius',
        'max_show_num',
    )
    readonly_fields = ('id',)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'user',
        'name',
        'saved_time',
        'linkUrl',
        'imageUrl',
        'latitude',
        'longtitude',
    )
    readonly_fields = ('id',)
