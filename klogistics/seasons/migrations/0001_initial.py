# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-10 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('state', models.CharField(choices=[(b'0', b'chiusa'), (b'1', b'aperta')], max_length=6)),
                ('available', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=30)),
                ('slug', models.SlugField(max_length=30)),
            ],
        ),
    ]
