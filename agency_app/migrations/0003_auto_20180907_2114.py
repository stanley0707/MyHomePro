# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-09-07 21:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency_app', '0002_auto_20180907_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='dir_img',
            field=models.CharField(default='33066', max_length=50, verbose_name='название папки'),
        ),
        migrations.AlterField(
            model_name='property',
            name='id_prop',
            field=models.CharField(blank=True, default='33066', max_length=150, null=True, verbose_name='id объекта/папки'),
        ),
        migrations.AlterField(
            model_name='propertystatistic',
            name='views',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Просмотры'),
        ),
    ]
