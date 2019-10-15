import uuid
from json import JSONEncoder
from uuid import UUID
from django.db import models
from django.utils import timezone


JSONEncoder_olddefault = JSONEncoder.default


def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID):
        return str(o)
    return JSONEncoder_olddefault(self, o)


JSONEncoder.default = JSONEncoder_newdefault


class AppUser(models.Model):
    """
    ユーザーのモデル
    """
    class Meta:
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    username = models.CharField(
        "ユーザー名",
        max_length=20,
        help_text="ユーザーの名前",
        unique=True)
    password = models.CharField(
        "パスワード",
        default=500,
        max_length=255,
        help_text="8~15文字の間")
    last_login = models.DateTimeField(
        "最終ログイン",
        default=timezone.now
    )

    def __str__(self):
        return self.username
