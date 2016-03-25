# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='servers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=100)),
                ('hostname', models.CharField(max_length=100)),
                ('task', models.CharField(max_length=100)),
                ('inUse', models.BooleanField(default=False)),
            ],
        ),
    ]
