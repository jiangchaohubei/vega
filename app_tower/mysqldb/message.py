#!/usr/bin/env python
# -*- coding:utf8 -*-
from app_tower.models import User,T_MESSAGE,T_MESSAGE_User_ID
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from json import dumps
import json
from django.core import serializers
import traceback
import logging
log = logging.getLogger("project")

#查询消息
def message_select(request):
    try:
        user=User.objects.get(id=int(request.session['userId']))
        messages=user.messages.all()
        total=len(messages)
        list = messages[0:5]
        messageList = serializers.serialize('json', list, ensure_ascii=False)

        true = True
        false=False
        null = None
    except Exception,ex:
        print Exception, ex
        traceback.print_exc()
        log.error(ex.__str__())


    return HttpResponse(json.dumps({'resultCode':'0000','messageNum':total,'messageList': eval(messageList)}))

#清空消息
def message_clear(request):

    user=User.objects.get(id=int(request.session['userId']))
    user.messages.all().delete()

    return HttpResponse(json.dumps({'resultCode':'0000','resultDesc':'清空消息成功'}))