# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-28 18:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aberdeengo', '0011_remove_schedule_events'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='event',
        ),
        migrations.AddField(
            model_name='schedule',
            name='events',
            field=models.ManyToManyField(through='aberdeengo.ScheduleEntry', to='aberdeengo.Event'),
        ),
    ]
