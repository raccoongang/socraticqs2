# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0003_auto_20151229_0830'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueLabel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=200)),
                ('color', models.CharField(default=b'ffffff', max_length=6)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='issue',
            name='status',
        ),
        migrations.RemoveField(
            model_name='issue',
            name='tags',
        ),
        migrations.DeleteModel(
            name='IssueTag',
        ),
        migrations.AddField(
            model_name='issue',
            name='is_open',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='labels',
            field=models.ManyToManyField(to='ui.IssueLabel', null=True, blank=True),
            preserve_default=True,
        ),
    ]
