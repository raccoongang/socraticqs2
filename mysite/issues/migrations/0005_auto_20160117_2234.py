# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0004_auto_20160117_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issuelabel',
            name='color',
            field=models.CharField(default=b'Grey', max_length=20, choices=[(b'label-default', b'Grey'), (b'label-primary', b'Blue'), (b'label-success', b'Green'), (b'label-info', b'LightBlue'), (b'label-warning', b'Yellow'), (b'label-danger', b'Red')]),
            preserve_default=True,
        ),
    ]
