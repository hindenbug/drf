# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_user_invite_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_reset_token',
            field=models.CharField(blank=True, max_length=40, null=True, unique=True),
        ),
    ]
