#!/usr/bin/env python
# -*- coding:utf8 -*-
from app_tower.models import User,T_MESSAGE,T_MESSAGE_User_ID
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from json import dumps
import json
from django.core import serializers

#查询消息
def message_select(request):
    user=User.objects.get(id=int(request.session['userId']))
    messages=user.messages.all()
    messageList = serializers.serialize('json', messages, ensure_ascii=False)
    total=len(messageList)
    list = messageList[0:5]
    true = True
    false=False
    null = None

    return HttpResponse(json.dumps({'resultCode':'0000','messageNum':total,'messageList': eval(list)}))

#清空消息
def message_clear(request):

    user=User.objects.get(id=int(request.session['userId']))
    user.messages.all().delete()

    return HttpResponse(json.dumps({'resultCode':'0000','resultDesc':'清空消息成功'}))