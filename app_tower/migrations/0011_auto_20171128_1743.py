# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tower', '0010_auto_20171127_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_host',
            name='ARGS1',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='t_host',
            name='ARGS2',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='t_host',
            name='ARGS3',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
    ]
