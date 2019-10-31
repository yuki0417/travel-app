import uuid
from uuid import UUID
from json import JSONEncoder

from django.utils import timezone
from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)

from accounts.models import AppUser


JSONEncoder_olddefault = JSONEncoder.default


def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID):
        return str(o)


JSONEncoder.default = JSONEncoder_newdefault


class Setting(models.Model):
    """
    設定のモデル
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE)
    name = models.CharField(
        "設定名",
        max_length=20,
        help_text="設定の名称")
    radius = models.IntegerField(
        "半径",
        default=500,
        validators=[MinValueValidator(10), MaxValueValidator(10000)],
        help_text="現在地からの半径をm単位で指定する。10~10000の間で指定。")
    max_show_num = models.IntegerField(
        "最大表示件数",
        default=5,
        validators=[MaxValueValidator(500)],
        help_text="最大で表示する件数。最大値は500。")

    class Meta:
        verbose_name = '設定'
        verbose_name_plural = '設定'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name="name_must_be_unique")
        ]


class Place(models.Model):
    """
    気になる場所リストのモデル
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE)
    name = models.CharField(
        "場所名",
        max_length=255,
        help_text="場所の名称")
    saved_time = models.DateTimeField(
        "保存日時",
        default=timezone.now,
        help_text="保存された時刻")
    linkUrl = models.URLField(
        "記事URL",
        blank=True,
        null=True,
        help_text="リンク先のURL")
    imageUrl = models.URLField(
        "画像URL",
        blank=True,
        null=True,
        help_text="サムネイル画像のURL")
    extract = models.CharField(
        "説明",
        max_length=256,
        blank=True,
        null=True,
        help_text="場所の簡単な説明"
    )
    latitude = models.FloatField(
        "緯度",
        default=0,
        blank=True,
        null=True,
        help_text="10進数表記")
    longtitude = models.FloatField(
        "経度",
        default=0,
        blank=True,
        null=True,
        help_text="10進数表記")

    class Meta:
        verbose_name = '気になる場所リスト'
        verbose_name_plural = '気になる場所リスト'

    def __str__(self):
        return self.name
