# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-19 16:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psa', '0006_auto_20180512_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='customcode',
            name='next_page',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
