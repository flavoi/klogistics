# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-09 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_auto_20160813_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='rank',
            field=models.CharField(choices=[('1', 'stagista'), ('2', 'consultant'), ('3', 'tech specialist'), ('4', 'senior'), ('5', 'assistant manager'), ('6', 'manager'), ('7', 'partner')], max_length=30),
        ),
    ]
