from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    FormView
)
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import (
    Place,
    Setting,
    Comment,
    SharedPlace,
    PlaceComment
)
from .forms import (
    SettingForm,
    SettingUpdateForm,
    CommentForm
)
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

    def mark_saved_place(self, user, place_raw_list):
        # 保存済みの場所であればフラグを追加する
        place_list = place_raw_list
        saved_places = Place.objects.filter(user=user)
        for place in place_list:
            try:
                if saved_places.get(name=place["name"]):
                    place["saved"] = True
            except Place.DoesNotExist:
                place["saved"] = False
        return place_list

    def post(self, request, *args, **kwargs):
        user_id = request.session.get('user_id', False)
        user = AppUser.objects.get(id=user_id)
        setting_now = request.POST.get('setting_now')
        location = request.POST.getlist('your_location[]')
        chosen_setting = Setting.objects.get(id=setting_now)
        radius = chosen_setting.radius
        max_show_num = chosen_setting.max_show_num

        # wikipediaAPIから検索
        place_raw_list = geo_search(location, radius, max_show_num)
        if place_raw_list is None:
            return render(request, 'travel/place_not_found.html')
        # 保存済みの場所かチェックする
        place_list = self.mark_saved_place(user, place_raw_list)
        d = {
            'your_location': location,
            'place_list': place_list,
            'radius': radius,
            'max_show_num': max_show_num,
        }
        return render(request, 'travel/place_result.html', d)


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
    form_class = SettingUpdateForm
    template_name = 'travel/setting_update_form.html'
    success_url = reverse_lazy('travel:setting_update_done')

    def get_object(self):
        return Setting.objects.get(id=self.kwargs['id'])


def setting_update_done(request):
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
    # 場所のお気に入りリスト追加AJAXの機能
    if request.method == 'POST':
        user_id = request.session.get('user_id', False)
        user = AppUser.objects.get(id=user_id)
        name = request.POST.get('name')
        linkUrl = request.POST.get('linkUrl')
        imageUrl = request.POST.get('imageUrl')
        extract = request.POST.get('extract')
        latitude = request.POST.get('latitude')
        longtitude = request.POST.get('longtitude')
        prefecture = request.POST.get('prefecture')
        city = request.POST.get('city')
        Place.objects.create(
            name=name,
            user=user,
            linkUrl=linkUrl,
            imageUrl=imageUrl,
            extract=extract,
            latitude=latitude,
            longtitude=longtitude,
            prefecture=prefecture,
            city=city,
        )
        return render(request, 'travel/place_result.html')


def place_delete(request):
    # 場所のお気に入りリストから取り消しAJAXの機能
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


class SharePlaceView(FormView):
    """
    シェアする場所作成の画面
    """
    model = Comment
    form_class = CommentForm
    template_name = 'travel/comment_form.html'

    def get_object(self):
        return Place.objects.get(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["place"] = self.get_object()
        return context

    def post(self, request, *args, **kwargs):
        comment = {
            "user": request.POST["user"],
            "comment": request.POST["comment"],
            "pub_date": request.POST["pub_date"],
        }
        # コメントを保存
        com_obj = self.save_comment(comment)
        place = {
            "name": request.POST["place_name"],
            "linkUrl": request.POST["linkUrl"],
            "imageUrl": request.POST["imageUrl"],
            "extract": request.POST["extract"],
            "latitude": request.POST["latitude"],
            "longtitude": request.POST["longtitude"],
            "prefecture": request.POST["prefecture"],
            "city": request.POST["city"],
        }
        # 場所テーブルに追記
        self.add_to_sharedplace(place)
        # コメントと場所をむすびつける
        self.connect_comment_place(place, com_obj)

        return render(request, 'travel/share_place_done.html')

    def save_comment(self, comment):
        com_obj = Comment.objects.create(
            user=AppUser.objects.get(id=comment["user"]),
            comment=comment["comment"],
            pub_date=comment["pub_date"],
        )
        com_obj.save()
        return com_obj

    def add_to_sharedplace(self, place):
        # すでに登録されているか確認
        try:
            SharedPlace.objects.get(name=place["name"])
        except SharedPlace.DoesNotExist:
            SharedPlace.objects.create(
                name=place["name"],
                linkUrl=place["linkUrl"],
                imageUrl=place["imageUrl"],
                extract=place["extract"],
                latitude=place["latitude"],
                longtitude=place["longtitude"],
                prefecture=place["prefecture"],
                city=place["city"],
            )

    def connect_comment_place(self, place, com_obj):
        PlaceComment.objects.create(
            share_place=place["name"],
            comment=Comment.objects.get(id=com_obj.pk),
        )


class SharedPlaceListView(ListView):
    """
    シェアされた場所の一覧画面
    """
    template_name = 'travel/shared_place_list.html'

    def queryset(self):
        user_id = self.request.session.get('user_id', False)
        place_list = self.get_place_comment_list(user_id)
        return place_list

    def mark_saved_place(self, place, user_id):
        # 保存済みの場所であればフラグを追加する
        try:
            if Place.objects.get(name=place, user=user_id):
                return True
        except Place.DoesNotExist:
            return False

    def get_place_comment_list(self, user_id):
        place_comment_list = []
        for obj in SharedPlace.objects.all():
            place_comment = {
                'name': obj.name,
                'linkUrl': obj.linkUrl,
                'imageUrl': obj.imageUrl,
                'extract': obj.extract,
                'latitude': obj.latitude,
                'longtitude': obj.longtitude,
            }
            place_comment["saved"] = self.mark_saved_place(
                place_comment['name'], user_id)
            comment = PlaceComment.objects.filter(share_place=obj.name)
            place_comment['comment'] = comment
            place_comment_list.append(place_comment)

        return place_comment_list
