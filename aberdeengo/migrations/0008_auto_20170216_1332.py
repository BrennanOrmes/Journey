# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-16 13:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aberdeengo', '0007_schedule_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='schedule',
        ),
        migrations.AddField(
            model_name='customuser',
            name='schedule',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='aberdeengo.Schedule'),
        ),
    ]