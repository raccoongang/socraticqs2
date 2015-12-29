# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ct', '0016_auto_20150626_0301'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(max_length=120, choices=[(b'warning', b'warning'), (b'propose', b'propose'), (b'enhance', b'enhance'), (b'off-target', b'off-target'), (b'bug', b'bug'), (b'diagnose', b'diagnose'), (b'resolve', b'resolve')])),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('assignee', models.ForeignKey(related_name='assignee', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(related_name='author', to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(blank=True, to='ct.Course', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IssueTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=120)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='issue',
            name='tags',
            field=models.ManyToManyField(to='ui.IssueTag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='unit',
            field=models.ForeignKey(blank=True, to='ct.Unit', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='unit_lesson',
            field=models.ForeignKey(blank=True, to='ct.UnitLesson', null=True),
            preserve_default=True,
        ),
    ]
