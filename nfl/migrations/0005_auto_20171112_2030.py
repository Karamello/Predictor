# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 20:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nfl', '0004_remove_game_stadium'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='nfl_id',
            field=models.IntegerField(db_index=True, unique=True),
        ),
    ]