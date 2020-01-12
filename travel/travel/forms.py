from django import forms
from .models import Setting, Comment


class SettingForm(forms.ModelForm):
    """
    設定登録画面用のフォーム
    """
    class Meta:
        model = Setting
        fields = ('user', 'name', 'radius', 'max_show_num')
        widgets = {
            'user': forms.HiddenInput(),
        }

    def clean(self):
        super().clean()
        user = self.cleaned_data.get('user', None)
        tmp_setting_name = self.cleaned_data.get('name', None)
        try:
            Setting.objects.get(user=user, name=tmp_setting_name)
            self.add_error('name', '同じ設定名が存在します。違う設定名に変更してください。')
        except Setting.DoesNotExist:
            pass


class SettingUpdateForm(forms.ModelForm):
    """
    設定更新画面用のフォーム
    """
    class Meta:
        model = Setting
        fields = ('user', 'name', 'radius', 'max_show_num')
        widgets = {
            'user': forms.HiddenInput(),
        }

    def clean(self):
        super().clean()
        user = self.cleaned_data.get('user', None)
        new_setting_name = self.cleaned_data.get('name', None)
        old_setting_name = self.instance.name
        # 他の設定に設定名が使われていた場合
        if not new_setting_name == old_setting_name:
            try:
                Setting.objects.get(user=user, name=new_setting_name)
                self.add_error('name', '同じ設定名が存在します。違う設定名に変更してください。')
            except Setting.DoesNotExist:
                pass


class CommentForm(forms.ModelForm):
    """
    場所のコメントを登録するフォーム
    """
    class Meta:
        model = Comment
        fields = (
            'user',
            'comment',
            'pub_date'
        )
        widgets = {
            'user': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].widget.attrs['readonly'] = True
