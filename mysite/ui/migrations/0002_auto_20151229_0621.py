# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='tags',
            field=models.ManyToManyField(to='ui.IssueTag', null=True, blank=True),
            preserve_default=True,
        ),
    ]
