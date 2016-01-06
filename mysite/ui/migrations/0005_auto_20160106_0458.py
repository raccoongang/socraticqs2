# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0004_auto_20151230_0633'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='affected_count',
            field=models.PositiveIntegerField(default=1, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='auto_issue',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
