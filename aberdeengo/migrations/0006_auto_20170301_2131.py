# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-01 21:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aberdeengo', '0005_event_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='tags',
            new_name='eventTags',
        ),
    ]
