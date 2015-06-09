# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lti', '0003_auto_20150529_0552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ltiuser',
            name='course_id',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
