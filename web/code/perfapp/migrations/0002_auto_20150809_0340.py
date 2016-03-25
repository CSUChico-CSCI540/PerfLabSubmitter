# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servers',
            name='csrf',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='servers',
            name='hostname',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='servers',
            name='task',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
