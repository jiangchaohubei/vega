#!/usr/bin/env python
# -*- coding:utf8 -*-
from django.apps import AppConfig


class ExampleConfig(AppConfig):
    name = 'app_tower'

    def ready(self):
        import app_tower.signals