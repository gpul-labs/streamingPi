# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-09 11:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DarkiceConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bitrateMode', models.CharField(max_length=3)),
                ('format', models.CharField(max_length=20)),
                ('bitrate', models.CharField(max_length=8)),
                ('server', models.CharField(max_length=60)),
                ('port', models.CharField(max_length=6)),
                ('password', models.CharField(max_length=30)),
                ('mountPoint', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=300)),
                ('url', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=30)),
                ('public', models.CharField(max_length=3)),
                ('localDumpFile', models.CharField(max_length=40)),
            ],
        ),
    ]