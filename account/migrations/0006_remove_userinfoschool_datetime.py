# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-31 06:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20181231_0555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfoschool',
            name='datetime',
        ),
    ]
