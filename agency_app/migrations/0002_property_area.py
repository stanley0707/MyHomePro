# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-07-30 07:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='area',
            field=models.PositiveIntegerField(default=0, verbose_name='метраж'),
        ),
    ]
