# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0016_auto_20150626_0301'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='description_html',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lesson',
            name='text_html',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='response',
            name='text_html',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
