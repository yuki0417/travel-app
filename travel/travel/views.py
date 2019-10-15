from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import Place, Setting
from .forms import SettingForm
from .wikipedia import geo_search
from accounts.models import AppUser


class PlaceListView(ListView):
    """
    場所情報表示画面
    """
    template_name = 'travel/place_list.html'
    setting_radius_meta = Setting._meta.get_field('radius').verbose_name
    setting_max_show_num_meta = \
        Setting._meta.get_field('max_show_num').verbose_name

    # 利用するモデルを指定
    def get_queryset(self):
        user_id = self.request.session.get('user_id', False)
        return Setting.objects.filter(user=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['setting_radius_meta'] = self.setting_radius_meta
        context['setting_max_show_num_meta'] = self.setting_max_show_num_meta
        return context

    def search_saved_place(self, user, place_raw_list):
        place_list = place_raw_list
        saved_places = Place.objects.filter(user=user)
        for place in place_list:
            try:
                if saved_places.get(name=place["name"]):
                    place["saved"] = True
            except Place.DoesNotExist:
                pass
        return place_list

    def post(self, request, *args, **kwargs):
        user_id = request.session.get('user_id', False)
        user = AppUser.objects.get(id=user_id)
        setting_now = request.POST.get('setting_now')
        location = request.POST.getlist('your_location[]')

        if location and setting_now:
            if setting_now:
                chosenSetting = Setting.objects.get(id=setting_now)
                radius = chosenSetting.radius
                max_show_num = chosenSetting.max_show_num
            else:
                radius = 1000
                max_show_num = 3

            # wikipediaAPIから検索
            place_raw_list = geo_search(location, radius, max_show_num)
            if place_raw_list is None:
                return render(request, 'travel/place_not_found.html')
            place_list = self.search_saved_place(user, place_raw_list)
            d = {
                'your_location': location,
                'place_list': place_list,
                'radius': radius,
                'max_show_num': max_show_num,
                'object_list': self.get_queryset(),
                'setting_radius_meta': self.setting_radius_meta,
                'setting_max_show_num_meta': self.setting_max_show_num_meta,
            }
            return render(request, 'travel/place_result.html', d)
        else:
            d = {
                'object_list': self.get_queryset(),
                'setting_radius_meta': self.setting_radius_meta,
                'setting_max_show_num_meta': self.setting_max_show_num_meta,
            }
            return render(request, self.template_name, d)


class SettingCreateView(CreateView):
    """
    設定作成用ビュー
    """
    model = Setting
    form_class = SettingForm
    template_name = 'travel/setting_form.html'
    success_url = reverse_lazy('travel:done_setting')


def setting_done(request):
    return render(request, 'travel/setting_done.html')


class SettingListView(ListView):
    """
    設定情報の一覧画面
    """
    model = Setting
    template_name = 'travel/setting_list.html'

    def queryset(self):
        user_id = self.request.session.get('user_id')
        return Setting.objects.filter(user=user_id)


class SettingUpdateView(UpdateView):
    """
    設定の更新画面
    """
    model = Setting
    form_class = SettingForm
    success_url = reverse_lazy('travel:setting_update_done')

    def get_object(self):
        return Setting.objects.get(id=self.kwargs['id'])


def update_done(request):
    return render(request, 'travel/setting_update_done.html')


class SettingDeleteView(DeleteView):
    """
    設定の削除画面
    """
    model = Setting
    success_url = reverse_lazy('travel:setting_delete_done')

    def get_object(self):
        return Setting.objects.get(id=self.kwargs['id'])


def delete_done(request):
    return render(request, 'travel/setting_delete_done.html')


def place_save(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id', False)
        user = AppUser.objects.get(id=user_id)
        name = request.POST.get('name')
        linkurl = request.POST.get('linkurl')
        imageUrl = request.POST.get('imageUrl')
        extract = request.POST.get('extract')
        latitude = request.POST.get('latitude')
        longtitude = request.POST.get('longtitude')
        Place.objects.create(
            name=name,
            user=user,
            linkUrl=linkurl,
            imageUrl=imageUrl,
            extract=extract,
            latitude=latitude,
            longtitude=longtitude,
        )
        return render(request, 'travel/place_result.html')


def place_delete(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id', False)
        user = AppUser.objects.get(id=user_id)
        name = request.POST.get('name')
        Place.objects.get(user=user, name=name).delete()
        return render(request, 'travel/place_result.html')


class SavedPlaceListView(ListView):
    """
    気になるリストの一覧画面
    """
    template_name = 'travel/saved_place_list.html'

    def get_queryset(self):
        user_id = self.request.session.get('user_id', False)
        return Place.objects.filter(user=user_id)
