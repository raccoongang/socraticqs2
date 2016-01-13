# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0006_issuecomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='assignee',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='author',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='course',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='labels',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='unit_lesson',
        ),
        migrations.RemoveField(
            model_name='issuecomment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='issuecomment',
            name='issue',
        ),
        migrations.DeleteModel(
            name='Issue',
        ),
        migrations.RemoveField(
            model_name='issuecomment',
            name='parent',
        ),
        migrations.DeleteModel(
            name='IssueComment',
        ),
        migrations.DeleteModel(
            name='IssueLabel',
        ),
    ]
