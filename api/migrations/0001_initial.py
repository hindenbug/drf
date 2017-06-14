# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 13:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, unique=True)),
            ],
            options={
                'db_table': 'teams',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.EmailField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('verified', models.BooleanField(default=False)),
                ('password', models.CharField(blank=True, max_length=32)),
                ('team', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='api.Team')),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
