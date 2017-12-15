# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tower', '0009_auto_20171124_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_module',
            name='NAME',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='t_software',
            name='NAME',
            field=models.CharField(max_length=128),
        ),
    ]
