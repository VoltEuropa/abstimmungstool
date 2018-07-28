# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-07-27 07:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initadmin', '0006_auto_20180723_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='userconfig',
            name='language_preference',
            field=models.CharField(choices=[('de', 'German'), ('en', 'English')], default='en', max_length=100),
        ),
    ]
