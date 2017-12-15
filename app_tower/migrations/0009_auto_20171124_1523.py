# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_tower', '0008_auto_20171120_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='T_MODULE',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('NAME', models.CharField(unique=True, max_length=128)),
                ('RESPONSIBLE_PERSON', models.CharField(max_length=32, null=True, blank=True)),
                ('DESCRIPTION', models.CharField(max_length=256, null=True, blank=True)),
                ('OWNER_ID', models.IntegerField(null=True, blank=True)),
                ('OWNER_NAME', models.CharField(max_length=128, null=True, blank=True)),
                ('OWNER_PROJECT_ID', models.IntegerField(null=True, blank=True)),
                ('OWNER_ALL', models.BooleanField(default=False)),
                ('CREATE_TIME', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('CREATE_USER_ID', models.IntegerField(null=True, blank=True)),
                ('CREATE_USER_NAME', models.CharField(max_length=128, null=True, blank=True)),
                ('LAST_MODIFY_TIME', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('MODIFY_USER_ID', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='T_SOFTWARE',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('NAME', models.CharField(unique=True, max_length=128)),
                ('RESPONSIBLE_PERSON', models.CharField(max_length=32, null=True, blank=True)),
                ('DESCRIPTION', models.CharField(max_length=256, null=True, blank=True)),
                ('LISTEN_PORT', models.IntegerField(null=True, blank=True)),
                ('DEPLOY_DIR', models.CharField(max_length=256, null=True, blank=True)),
                ('DEPLOY_ACCOUNT', models.CharField(max_length=32, null=True, blank=True)),
                ('TIMER_SCRIPT', models.CharField(max_length=512, null=True, blank=True)),
                ('LOG_EXPORT', models.CharField(max_length=512, null=True, blank=True)),
                ('NOTE', models.CharField(max_length=512, null=True, blank=True)),
                ('DATA_BACKUPPATH', models.CharField(max_length=512, null=True, blank=True)),
                ('DATA_FILEPATH', models.CharField(max_length=512, null=True, blank=True)),
                ('OWNER_ID', models.IntegerField(null=True, blank=True)),
                ('OWNER_NAME', models.CharField(max_length=128, null=True, blank=True)),
                ('OWNER_PROJECT_ID', models.IntegerField(null=True, blank=True)),
                ('OWNER_ALL', models.BooleanField(default=False)),
                ('CREATE_TIME', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('CREATE_USER_ID', models.IntegerField(null=True, blank=True)),
                ('CREATE_USER_NAME', models.CharField(max_length=128, null=True, blank=True)),
                ('LAST_MODIFY_TIME', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('MODIFY_USER_ID', models.IntegerField(null=True, blank=True)),
                ('ARGS1', models.CharField(max_length=128, null=True, blank=True)),
                ('ARGS2', models.CharField(max_length=128, null=True, blank=True)),
                ('ARGS3', models.CharField(max_length=128, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='T_SOFTWARE_HOST_ID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ISCOLONY', models.BooleanField(default=False)),
                ('LINEAR_ADDRESS', models.CharField(max_length=128, null=True, blank=True)),
                ('INTERNET_ADDRESS', models.CharField(max_length=128, null=True, blank=True)),
                ('DOMAIN_NAME', models.CharField(max_length=128, null=True, blank=True)),
                ('LISTEN_PORT', models.IntegerField(null=True, blank=True)),
                ('DEPLOY_DIR', models.CharField(max_length=256, null=True, blank=True)),
                ('DEPLOY_ACCOUNT', models.CharField(max_length=32, null=True, blank=True)),
                ('HOST_ID', models.ForeignKey(related_name='HOST_ID_T_SOFTWARE_HOST_ID', to='app_tower.T_HOST')),
                ('SOFTWARE_ID', models.ForeignKey(related_name='SOFTWARE_ID_T_SOFTWARE_HOST_ID', to='app_tower.T_SOFTWARE')),
            ],
        ),
        migrations.CreateModel(
            name='T_SYSTEM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('NAME', models.CharField(unique=True, max_length=128)),
                ('COMPANY', models.CharField(max_length=64, null=True, blank=True)),
                ('DESCRIPTION', models.CharField(max_length=256, null=True, blank=True)),
                ('OWNER_ID', models.IntegerField(null=True, blank=True)),
                ('OWNER_NAME', models.CharField(max_length=128, null=True, blank=True)),
                ('OWNER_PROJECT_ID', models.IntegerField(null=True, blank=True)),
                ('OWNER_ALL', models.BooleanField(default=False)),
                ('CREATE_TIME', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('CREATE_USER_ID', models.IntegerField(null=True, blank=True)),
                ('CREATE_USER_NAME', models.CharField(max_length=128, null=True, blank=True)),
                ('LAST_MODIFY_TIME', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('MODIFY_USER_ID', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='T_VERSION',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('NAME', models.FloatField()),
                ('DESCRIPTION', models.CharField(max_length=256, null=True, blank=True)),
                ('INSTALL_PATH', models.CharField(max_length=256, null=True, blank=True)),
                ('PACKAGE_PATH', models.CharField(max_length=256, null=True, blank=True)),
                ('ISUSE', models.BooleanField(default=True)),
                ('OWNER_ID', models.IntegerField(null=True, blank=True)),
                ('OWNER_NAME', models.CharField(max_length=128, null=True, blank=True)),
                ('OWNER_PROJECT_ID', models.IntegerField(null=True, blank=True)),
                ('OWNER_ALL', models.BooleanField(default=False)),
                ('CREATE_TIME', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('CREATE_USER_ID', models.IntegerField(null=True, blank=True)),
                ('CREATE_USER_NAME', models.CharField(max_length=128, null=True, blank=True)),
                ('LAST_MODIFY_TIME', models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('MODIFY_USER_ID', models.IntegerField(null=True, blank=True)),
                ('ARGS1', models.CharField(max_length=128, null=True, blank=True)),
                ('ARGS2', models.CharField(max_length=128, null=True, blank=True)),
                ('ARGS3', models.CharField(max_length=128, null=True, blank=True)),
                ('SOFTWARE_ID', models.ForeignKey(related_name='SOFTWARE_ID_T_VERSION', on_delete=django.db.models.deletion.PROTECT, blank=True, to='app_tower.T_SOFTWARE', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='t_software',
            name='HOSTS',
            field=models.ManyToManyField(to='app_tower.T_HOST', through='app_tower.T_SOFTWARE_HOST_ID'),
        ),
        migrations.AddField(
            model_name='t_software',
            name='MODULE_ID',
            field=models.ForeignKey(related_name='MODULE_ID_T_SOFTWARE', on_delete=django.db.models.deletion.PROTECT, blank=True, to='app_tower.T_MODULE', null=True),
        ),
        migrations.AddField(
            model_name='t_module',
            name='SYSTEM_ID',
            field=models.ForeignKey(related_name='SYSTEM_ID_T_MODULE', on_delete=django.db.models.deletion.PROTECT, blank=True, to='app_tower.T_SYSTEM', null=True),
        ),
        migrations.AddField(
            model_name='t_host',
            name='SYSTEM_ID',
            field=models.ForeignKey(related_name='SYSTEM_ID_T_HOST', on_delete=django.db.models.deletion.PROTECT, blank=True, to='app_tower.T_SYSTEM', null=True),
        ),
    ]
