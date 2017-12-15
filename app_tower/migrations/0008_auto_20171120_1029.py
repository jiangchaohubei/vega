# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tower', '0007_auto_20171108_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_host',
            name='CUTTER_NUMBER',
            field=models.CharField(max_length=128, null=True, verbose_name=b'\xe5\x88\x80\xe6\xa1\x86\xe7\xbc\x96\xe5\x8f\xb7', blank=True),
        ),
        migrations.AddField(
            model_name='t_host',
            name='MACHINE_POSITION',
            field=models.CharField(max_length=128, null=True, verbose_name=b'\xe6\x9c\xba\xe6\x9e\xb6\xe4\xbd\x8d\xe7\xbd\xae', blank=True),
        ),
        migrations.AddField(
            model_name='t_host',
            name='MACHINE_ROOM',
            field=models.CharField(max_length=128, null=True, verbose_name=b'\xe6\x9c\xba\xe6\x88\xbf', blank=True),
        ),
        migrations.AddField(
            model_name='t_host',
            name='MACHINE_TYPE',
            field=models.CharField(max_length=128, null=True, verbose_name=b'\xe6\x9c\xba\xe5\x99\xa8\xe7\xb1\xbb\xe5\x9e\x8b', blank=True),
        ),
        migrations.AddField(
            model_name='t_host',
            name='NOTE',
            field=models.CharField(max_length=128, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True),
        ),
        migrations.AddField(
            model_name='t_host',
            name='OS',
            field=models.CharField(max_length=128, null=True, verbose_name=b'os', blank=True),
        ),
        migrations.AddField(
            model_name='t_host',
            name='PHYSICAL_MACHINE_TYPE',
            field=models.CharField(max_length=128, null=True, verbose_name=b'\xe7\x89\xa9\xe7\x90\x86\xe6\x9c\xba\xe9\x85\x8d\xe7\xbd\xae\xe7\xb1\xbb\xe5\x9e\x8b', blank=True),
        ),
        migrations.AddField(
            model_name='t_host',
            name='SN_NUMBER',
            field=models.CharField(max_length=128, null=True, verbose_name=b'SN\xe5\x8f\xb7', blank=True),
        ),
    ]
