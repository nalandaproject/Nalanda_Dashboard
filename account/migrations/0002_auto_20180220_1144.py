# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-20 11:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    """operations = [
        migrations.RemoveField(
            model_name='masterylevelstudent',
            name='completed',
        ),
        migrations.AddField(
            model_name='content',
            name='sub_topics_total',
            field=models.IntegerField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='masterylevelstudent',
            name='mastered',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='latestfetchdate',
            name='date_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]"""