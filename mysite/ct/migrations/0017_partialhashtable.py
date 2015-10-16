# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0016_auto_20150626_0301'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartialHashTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=64)),
                ('params', models.TextField()),
            ],
            options={
                'verbose_name': 'PartialHashTable',
                'verbose_name_plural': 'PartialHashTables',
            },
            bases=(models.Model,),
        ),
    ]
