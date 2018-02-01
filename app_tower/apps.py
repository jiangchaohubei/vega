#!/usr/bin/env python
# -*- coding:utf8 -*-
from django.apps import AppConfig


class ExampleConfig(AppConfig):
    name = 'app_tower'

    def ready(self):
        #signal初始化
        import app_tower.signals
        #权限配置初始化
        from vega.rolelist_permissionlist_init import rolelist_permission
        initRoleClass=rolelist_permission()
        initRoleClass.init_role_user()