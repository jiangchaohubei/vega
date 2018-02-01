#!/usr/bin/env python
# -*- coding:utf8 -*-
from app_tower.models import User,T_MESSAGE,T_MESSAGE_User_ID
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from json import dumps
import json
from django.core import serializers
import traceback
from django.utils.timezone import now, timedelta
import logging
log = logging.getLogger("message")

#查询消息
def message_init(request):
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


#description:查询历史消息
#params: request.GET {"limit":5,"offset":0,"order":"asc","ordername":"id","name":"","description":""}
#return: {"resultCode":"","resultDesc":"","rows":"","total":""}

def message_select(request):

    log.info("message_select start")
    log.info("request: "+str(request))
    response_data = {}
    try:
        #本页第一条数据下标
        offset= request.GET.get('offset')
        # 每页数量
        limit = request.GET.get('limit')
        # 排序asc，desc
        order= ''
        if request.GET.get('order')=='desc':
            order='-'
        ordername='id'
        if request.GET.get('ordername'):
            ordername= str(request.GET.get('ordername'))
        ordername.replace('fields.','')
        orderBy=order+ordername
        name = ''
        description = ''
        timeArea=''
        if request.GET.get("name"):
            name=request.GET.get("name")
        if request.GET.get("description"):
            description=request.GET.get("description")
        if request.GET.get("timeArea"):
            timeArea=request.GET.get("timeArea")

        # 排序字段
        # ordername= request.GET.get('ordername')
        # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM     Test.objects.filter(name="runoob").order_by("id")
        end = now().date()+timedelta(days=1)
        start =now().date() - timedelta(days=30)
        messageList=[]
        total=0
        user=User.objects.get(id=int(request.session['userId']))
        messages=user.messages.all()

        if timeArea=='today':
            end = now().date()+timedelta(days=1)
            start =now().date()

        elif timeArea=='week':
            end = now().date()+timedelta(days=1)
            start =now().date() - timedelta(days=7)

        elif timeArea=='month':
            end = now().date()+timedelta(days=1)
            start =now().date() - timedelta(days=30)

        messageList = messages.filter(CREATE_TIME__range=(start, end)).order_by(orderBy)
        total=len(messageList)
        print end,start
        list = messageList[int(offset):int(offset)+int(limit)]
        #[5:10]这是查找从下标5到下标10之间的数据，不包括10。

        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '查询成功！'
        #序列码 serializers.serialize，且ensure_ascii=False防止乱码
        response_data['rows'] = serializers.serialize('json', list,ensure_ascii=False,use_natural_keys=True)
        response_data['total'] = total
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    log.info('response_data:'+str(response_data))
    log.info("message_select end")
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")