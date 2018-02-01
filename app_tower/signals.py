#!/usr/bin/env python
# -*- coding:utf8 -*-
from django.db.models.signals import pre_save,post_save,post_delete
from django.dispatch import receiver
from app_tower.models import T_TOOL,User,T_MESSAGE,T_MESSAGE_User_ID
import json
from channels import Group
import django.dispatch
from django.db.models import Q
import logging
log = logging.getLogger("message")

#工具通过/不通过审核,自定义signal
tool_passaudit = django.dispatch.Signal(providing_args=["passaudit","toolname"])
def on_tool_passaudit(sender, **kwargs):
    if "passaudit" in kwargs:
        passaudit = kwargs.get("passaudit")
        toolname = kwargs.get("toolname")
        msg=""
        if passaudit:
            msg=u"工具[%s]通过审核" % toolname
            Group('User').send({
                'text': json.dumps({
                    'message':msg,
                    'type':'tool'

                })
            })
        else:
            msg=u"工具[%s]没有通过审核" % toolname
            Group('User').send({
                'text': json.dumps({
                    'message':msg,
                    'type':'tool'
                })
            })
        message=T_MESSAGE(CONTENT=msg,TYPE='tool')
        message.save()
        message_user_list = list()
        users=User.objects.all()
        for u in users:
            message_user_list.append(T_MESSAGE_User_ID(MESSAGE_ID=message,User_ID=u))
        T_MESSAGE_User_ID.objects.bulk_create(message_user_list)


tool_passaudit.connect(on_tool_passaudit)

@receiver(post_save, sender=T_TOOL)
def on_tool_add(sender, **kwargs):
    log.info("on_tool_add start")
    msg=u"有新的工具[%s]需要审核" % kwargs['instance'].__dict__['NAME']
    Group('Administrant').send({
        'text': json.dumps({
            'message':msg,
            'type':'tool'

        })
    })

    message=T_MESSAGE(CONTENT=msg,TYPE='tool')
    message.save()
    message_user_list = list()
    users=User.objects.all().filter(Q(role__name='超级管理员') | Q(role__name='管理员'))
    log.info(users)
    for u in users:
        message_user_list.append(T_MESSAGE_User_ID(MESSAGE_ID=message,User_ID=u))
    T_MESSAGE_User_ID.objects.bulk_create(message_user_list)
    log.info("on_tool_add end")

@receiver(post_delete, sender=T_TOOL)
def on_tool_delete(sender, **kwargs):
    msg=u"工具[%s]被删除" % kwargs['instance'].__dict__['NAME']
    Group('User').send({
        'text': json.dumps({
            'message':msg,
            'type':'tool'

        })
    })

    message=T_MESSAGE(CONTENT=msg,TYPE='tool')
    message.save()
    message_user_list = list()
    users=User.objects.all()
    for u in users:
        message_user_list.append(T_MESSAGE_User_ID(MESSAGE_ID=message,User_ID=u))
    T_MESSAGE_User_ID.objects.bulk_create(message_user_list)

# @receiver(pre_save, sender=T_TOOL)
# def on_tool_logout(sender, **kwargs):
#     T_TOOL.objects.filter(user=kwargs.get('user')).delete()