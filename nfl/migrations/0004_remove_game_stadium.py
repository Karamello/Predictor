# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 20:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0003_auto_20171112_2025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='stadium',
        ),
    ]
