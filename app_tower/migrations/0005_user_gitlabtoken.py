# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tower', '0004_playbook_filedir'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gitLabToken',
            field=models.CharField(max_length=512, null=True, blank=True),
        ),
    ]
