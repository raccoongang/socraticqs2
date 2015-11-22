# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import psa.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('psa', '0004_customcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenForgotPassword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(default=psa.models.create_token, max_length=32)),
                ('next_url', models.CharField(max_length=200)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
