# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-07-28 11:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('initproc', '0030_add-team-creation-date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammembership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to=settings.AUTH_USER_MODEL),
        ),
    ]
