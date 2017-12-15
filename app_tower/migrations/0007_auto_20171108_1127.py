# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tower', '0006_auto_20171103_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timertask',
            name='PERIODICTASK_ID',
            field=models.ForeignKey(related_name='PERIODICTASK_ID_TimerTask', blank=True, to='djcelery.PeriodicTask', null=True),
        ),
    ]
