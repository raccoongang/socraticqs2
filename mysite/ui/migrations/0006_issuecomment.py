# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ui', '0005_auto_20160106_0458'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('issue', models.ForeignKey(to='ui.Issue')),
                ('parent', models.ForeignKey(blank=True, to='ui.IssueComment', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
