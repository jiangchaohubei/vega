# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_tower', '0002_playbook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_job',
            name='PLAYBOOK_ID',
            field=models.ForeignKey(related_name='PLAYBOOK_ID_T_JOB', on_delete=django.db.models.deletion.PROTECT, blank=True, to='app_tower.playbook', null=True),
        ),
        migrations.AlterField(
            model_name='t_job_template',
            name='PLAYBOOK_ID',
            field=models.ForeignKey(related_name='PLAYBOOK_ID_T_JOB_TEMPLATE', on_delete=django.db.models.deletion.PROTECT, blank=True, to='app_tower.playbook', null=True),
        ),
    ]
