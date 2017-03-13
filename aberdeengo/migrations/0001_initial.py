# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-13 13:12
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('payment', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('location', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('public', models.BooleanField()),
                ('price', models.IntegerField(null=True)),
                ('publication_date', models.DateField(default=datetime.date.today, verbose_name=b'Date')),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('public', models.BooleanField()),
                ('price', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aberdeengo.Events')),
            ],
        ),
        migrations.CreateModel(
            name='Interests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordinates', models.FloatField(max_length=20)),
                ('name', models.CharField(max_length=255)),
                ('opentime', models.TimeField(null=True)),
                ('closedtime', models.TimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LocationTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aberdeengo.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('travelType', models.CharField(default=b'DRIVING', max_length=255)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aberdeengo.Event')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aberdeengo.Schedule')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='schedule',
            name='events',
            field=models.ManyToManyField(through='aberdeengo.ScheduleEntry', to='aberdeengo.Event'),
        ),
        migrations.AddField(
            model_name='locationtag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aberdeengo.Tag'),
        ),
        migrations.AddField(
            model_name='interests',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aberdeengo.Tag'),
        ),
        migrations.AddField(
            model_name='interests',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventtag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aberdeengo.Tag'),
        ),
        migrations.AddField(
            model_name='events',
            name='tags',
            field=models.ManyToManyField(to='aberdeengo.Tag'),
        ),
        migrations.AddField(
            model_name='event',
            name='eventTags',
            field=models.ManyToManyField(to='aberdeengo.Tag'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='aberdeengo.CustomUser'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='interests',
            field=models.ManyToManyField(to='aberdeengo.Tag'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='schedule',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='aberdeengo.Schedule'),
        ),
    ]
