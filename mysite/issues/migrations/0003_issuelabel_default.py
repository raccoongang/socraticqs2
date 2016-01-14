# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

DEFAULT_ISSUES = (('warning', 'warning'),
                  ('propose', 'propose'),
                  ('enhance', 'enhance'),
                  ('off-target', 'off-target'),
                  ('bug', 'bug'),
                  ('diagnose', 'diagnose'),
                  ('resolve', 'resolve'))


def make_default_labels(apps, schema_editor):
    Label = apps.get_model("issues", "IssueLabel")
    for each in DEFAULT_ISSUES:
        Label.objects.create(title=each[0],
                             description=each[1],
                             default=True)


def remove_default_labels(apps, schema_editor):
    Label = apps.get_model("issues", "IssueLabel")
    for each in DEFAULT_ISSUES:
        label = Label.objects.filter(title=each[0],
                                     description=each[1],
                                     default=True)
        label.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0002_auto_20160114_0254'),
    ]

    operations = [
        migrations.RunPython(make_default_labels, remove_default_labels),
    ]
