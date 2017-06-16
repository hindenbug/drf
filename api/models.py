# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

class Team(models.Model):
    class Meta:
        db_table = 'teams'

    name = models.CharField(max_length=50, blank=False, unique=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    class Meta:
        db_table = 'users'

    email = models.EmailField(max_length=50, blank=False, unique=True, primary_key=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    verified = models.BooleanField(default=False)
    password = models.CharField(max_length=255, blank=True)
    team = models.ForeignKey(Team, null=True, default=None, related_name='members')
    verification_key = models.CharField(max_length=32, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=40, unique=True, blank=True, null=True)
    invite_code = models.CharField(max_length=8, unique=True, blank=False, null=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
