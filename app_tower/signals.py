#!/usr/bin/env python
# -*- coding:utf8 -*-
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from app_tower.models import T_TOOL
import json
from channels import Group

@receiver(post_save, sender=T_TOOL)
def on_tool_add(sender, **kwargs):
    Group('users').send({
        'text': json.dumps({
            'message':u"有新的工具需要审核"

        })
    })


# @receiver(pre_save, sender=T_TOOL)
# def on_tool_logout(sender, **kwargs):
#     T_TOOL.objects.filter(user=kwargs.get('user')).delete()