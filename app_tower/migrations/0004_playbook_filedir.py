# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tower', '0003_auto_20171013_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='playbook',
            name='FILEDIR',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
