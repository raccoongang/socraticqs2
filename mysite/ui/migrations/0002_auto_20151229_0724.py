# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 29, 15, 24, 50, 885146, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='issue',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='issue',
            name='tags',
            field=models.ManyToManyField(to='ui.IssueTag', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='issue',
            name='unit',
            field=models.ForeignKey(blank=True, to='ct.CourseUnit', null=True),
            preserve_default=True,
        ),
    ]
