# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-10-22 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0027_auto_20180904_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='mc_simplified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='add_unit_aborts',
            field=models.BooleanField(default=False),
        ),
    ]
