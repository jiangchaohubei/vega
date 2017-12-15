# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djcelery', '0001_initial'),
        ('app_tower', '0005_user_gitlabtoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimerTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('NAME', models.CharField(unique=True, max_length=128)),
                ('DESCRIPTION', models.CharField(max_length=256, null=True, blank=True)),
                ('ISUSE', models.BooleanField(default=False)),
                ('START_TIME', models.DateTimeField(null=True, verbose_name=b'\xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('EXPIRES_TIME', models.DateTimeField(null=True, verbose_name=b'\xe8\xbf\x87\xe6\x9c\x9f\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('EVERY', models.IntegerField(null=True, blank=True)),
                ('PERIOD', models.CharField(max_length=24, null=True, blank=True)),
                ('OWNER_ID', models.IntegerField(null=True, blank=True)),
                ('OWNER_NAME', models.CharField(max_length=128, null=True, blank=True)),
                ('OWNER_PROJECT_ID', models.IntegerField(null=True, blank=True)),
                ('OWNER_ALL', models.BooleanField(default=False)),
                ('CREATE_TIME', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('CREATE_USER_ID', models.IntegerField(null=True, blank=True)),
                ('CREATE_USER_NAME', models.CharField(max_length=128, null=True, blank=True)),
                ('LAST_MODIFY_TIME', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('MODIFY_USER_ID', models.IntegerField(null=True, blank=True)),
                ('JOBTEMPLETE_ID', models.ForeignKey(related_name='JOBTEMPLETE_ID_TimerTask', on_delete=django.db.models.deletion.PROTECT, blank=True, to='app_tower.T_JOB_TEMPLATE', null=True)),
                ('PERIODICTASK_ID', models.ForeignKey(related_name='PERIODICTASK_ID_TimerTask', on_delete=django.db.models.deletion.PROTECT, blank=True, to='djcelery.PeriodicTask', null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='t_login_credentials',
            name='LOGIN_PWD',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='t_login_credentials',
            name='PRIVILEGE_PWD',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
