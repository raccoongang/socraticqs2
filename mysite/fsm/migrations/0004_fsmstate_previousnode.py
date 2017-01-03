# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fsm', '0003_auto_20151030_0416'),
    ]

    operations = [
        migrations.AddField(
            model_name='fsmstate',
            name='previousNode',
            field=models.ForeignKey(related_name='previousNode', blank=True, to='fsm.FSMNode', null=True),
            preserve_default=True,
        ),
    ]
