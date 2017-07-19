# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='inventories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='jobTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=128)),
                ('user', models.CharField(max_length=32)),
                ('playbook', models.CharField(max_length=1024)),
                ('inventories_id', models.ForeignKey(to='app_tower.inventories')),
            ],
        ),
        migrations.AddField(
            model_name='host',
            name='inventories_id',
            field=models.ForeignKey(to='app_tower.inventories'),
        ),
    ]
