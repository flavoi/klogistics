# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-18 20:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_auto_20161209_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='role',
        ),
    ]
