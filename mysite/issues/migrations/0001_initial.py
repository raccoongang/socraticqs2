# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
                ('is_open', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('affected_count', models.PositiveIntegerField(default=1, blank=True)),
                ('auto_issue', models.BooleanField(default=False)),
                ('assignee', models.ForeignKey(related_name='assignee', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('author', models.ForeignKey(related_name='author', to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(blank=True, to='ct.Course', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IssueComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('issue', models.ForeignKey(to='issues.Issue')),
                ('parent', models.ForeignKey(blank=True, to='issues.IssueComment', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        migrations.AddField(
            model_name='issue',
            name='labels',
            field=models.ManyToManyField(to='issues.IssueLabel', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='unit',
            field=models.ForeignKey(blank=True, to='ct.CourseUnit', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='issue',
            name='unit_lesson',
            field=models.ForeignKey(blank=True, to='ct.UnitLesson', null=True),
            preserve_default=True,
        ),
    ]
