# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-28 18:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aberdeengo', '0010_auto_20170228_1823'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='events',
        ),
    ]
