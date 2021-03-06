# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-06 21:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initproc', '0002_auto_20170606_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initiative',
            name='was_closed_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='went_public_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='went_to_discussion_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='went_to_voting_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
