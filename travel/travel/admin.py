from django.contrib import admin
from .models import (
    Place,
    Setting,
    Comment,
    SharedPlace,
    PlaceComment
)


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
        'prefecture',
        'city',
    )
    readonly_fields = ('id',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'user',
        'comment',
        'pub_date',
    )
    readonly_fields = ('id',)


@admin.register(SharedPlace)
class SharedPlaceAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'name',
        'linkUrl',
        'imageUrl',
        'latitude',
        'longtitude',
        'prefecture',
        'city',
    )
    readonly_fields = ('id',)


@admin.register(PlaceComment)
class PlaceCommentAdmin(admin.ModelAdmin):
    save_as = True
    list_display = (
        'share_place',
        'comment',
    )
    readonly_fields = ('id',)
