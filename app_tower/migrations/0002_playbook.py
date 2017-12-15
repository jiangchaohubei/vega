# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tower', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='playbook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('NAME', models.CharField(unique=True, max_length=128)),
                ('DESCRIPTION', models.CharField(max_length=256)),
                ('PLAYBOOK_PATH', models.CharField(max_length=256)),
                ('PLAYBOOK_CONTENT', models.TextField(null=True, blank=True)),
                ('CREATE_TIME', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('CREATE_USER_ID', models.IntegerField(null=True, blank=True)),
                ('CREATE_USER_NAME', models.CharField(max_length=128, null=True, blank=True)),
                ('LAST_MODIFY_TIME', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('MODIFY_USER_ID', models.IntegerField(null=True, blank=True)),
                ('OWNER_ID', models.IntegerField(null=True, blank=True)),
                ('OWNER_NAME', models.CharField(max_length=128, null=True, blank=True)),
                ('OWNER_PROJECT_ID', models.IntegerField(null=True, blank=True)),
                ('OWNER_ALL', models.BooleanField(default=False)),
            ],
        ),
    ]
