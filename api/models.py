# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Team(models.Model):
    class Meta:
        db_table = 'teams'

    name = models.CharField(max_length=50, blank=True, unique=True)

    def __str__(self):
        return self.name


class User(models.Model):
    class Meta:
        db_table = 'users'

    email = models.EmailField(max_length=50, blank=False, unique=True, primary_key=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    verified = models.BooleanField(default=False)
    password = models.CharField(max_length=32, blank=True)
    team = models.ForeignKey(Team, null=True, default=None, related_name='members')

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
