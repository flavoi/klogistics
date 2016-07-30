# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-30 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seasons', '0002_season_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='name',
            field=models.CharField(default='stagione', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='season',
            name='slug',
            field=models.SlugField(default='stagione', max_length=30),
            preserve_default=False,
        ),
    ]
