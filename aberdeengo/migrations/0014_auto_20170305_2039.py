# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-05 20:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aberdeengo', '0013_auto_20170305_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profilePicture',
            field=models.ImageField(null=True, upload_to=b'aberdeengo/picture/profile/%Y/%m/%d'),
        ),
    ]
