# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-06 11:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aberdeengo', '0008_auto_20170406_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='aberdeengo.CustomUser'),
        ),
    ]
