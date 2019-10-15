# Generated by Django 2.2.4 on 2019-10-11 14:20

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(help_text='ユーザーの名前', max_length=20, unique=True, verbose_name='ユーザー名')),
                ('password', models.CharField(default=500, help_text='8~15文字の間', max_length=255, verbose_name='パスワード')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='最終ログイン')),
            ],
            options={
                'verbose_name': 'ユーザー',
                'verbose_name_plural': 'ユーザー',
            },
        ),
    ]
