from django import forms
from .models import Setting


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.unique_error_message = \
            lambda m, u: u'同じ設定名が存在します。違う設定名に変更してください。'
