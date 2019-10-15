from django.urls import path
from . import views


app_name = "travel"

urlpatterns = [
    path('list/', views.PlaceListView.as_view(), name='place_list'),
    path(
        'create_setting/',
        views.SettingCreateView.as_view(),
        name='create_setting'),
    path('done_setting/', views.setting_done, name='done_setting'),
    path(
        'setting_list/',
        views.SettingListView.as_view(),
        name='setting_list'),
    path(
        'update_setting/<uuid:id>/',
        views.SettingUpdateView.as_view(),
        name='update_setting'),
    path(
        'setting_update_done/',
        views.update_done,
        name='setting_update_done'),
    path(
        'delete_setting/<uuid:id>/',
        views.SettingDeleteView.as_view(),
        name='delete_setting'),
    path(
        'setting_delete_done/',
        views.delete_done,
        name='setting_delete_done'),
    path('place_save/', views.place_save, name='place_save'),
    path('place_delete/', views.place_delete, name='place_delete'),
    path(
        'saved_place/',
        views.SavedPlaceListView.as_view(),
        name='saved_place'),
]
