#!/usr/bin/env python
# -*- coding:utf8 -*-
from django.db.models.signals import pre_save,post_save,post_delete
from django.dispatch import receiver
from app_tower.models import T_TOOL
import json
from channels import Group
import django.dispatch

#工具通过/不通过审核
tool_passaudit = django.dispatch.Signal(providing_args=["passaudit","toolname"])
def on_tool_passaudit(sender, **kwargs):
    if "passaudit" in kwargs:
        passaudit = kwargs.get("passaudit")
        toolname = kwargs.get("toolname")
        if passaudit:
            Group('User').send({
                'text': json.dumps({
                    'message':u"工具[%s]通过审核" % toolname

                })
            })
        else:
            Group('User').send({
                'text': json.dumps({
                    'message':u"工具[%s]没有通过审核" % toolname

                })
            })


tool_passaudit.connect(on_tool_passaudit)

@receiver(post_save, sender=T_TOOL)
def on_tool_add(sender, **kwargs):
    print str(kwargs['instance'].__dict__)
    Group('Administrant').send({
        'text': json.dumps({
            'message':u"有新的工具[%s]需要审核" % kwargs['instance'].__dict__['NAME']

        })
    })

@receiver(post_delete, sender=T_TOOL)
def on_tool_add(sender, **kwargs):
    print str(kwargs['instance'].__dict__)
    Group('User').send({
        'text': json.dumps({
            'message':u"工具[%s]被删除" % kwargs['instance'].__dict__['NAME']

        })
    })


# @receiver(pre_save, sender=T_TOOL)
# def on_tool_logout(sender, **kwargs):
#     T_TOOL.objects.filter(user=kwargs.get('user')).delete()