#!/usr/bin/env python
# -*- coding:utf8 -*-
from app_tower.models import T_HOST,T_PROJECT
from app_tower.models import T_SYSTEM,T_MODULE
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from json import dumps
import json
import traceback

from django.core import serializers
from authority.permission import PermissionVerify
import logging
log = logging.getLogger("module")


def module_add(request):
    log.info('module_add start')
    log.info("request: "+str(request))

    response_data={}
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    try:
        if request.POST['OWNER']=='onlyOne':
            OWNER_ID=request.session['userId']
            OWNER_NAME=request.session['username']
        elif request.POST['OWNER']=='all':
            OWNER_ALL=True
        else:
            if not T_PROJECT.objects.check_id(request,request.POST['OWNER']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"项目组没有使用权限！"}))
            OWNER_PROJECT_ID=request.POST['OWNER']
        if not T_SYSTEM.objects.check_id(request,request.POST['SYSTEM_ID']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"系统没有使用权限！"}))

        if T_MODULE.objects.filter(NAME=request.POST['NAME'],SYSTEM_ID_id=int(request.POST['SYSTEM_ID'])).exists():
            response_data['resultCode']='0001'
            response_data['resultDesc']='系统中该模块已经存在，名称不能重复！'
            return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

        module = T_MODULE(NAME=request.POST['NAME'], DESCRIPTION=request.POST['DESCRIPTION'],SYSTEM_ID=T_SYSTEM.objects.get(id=request.POST['SYSTEM_ID']),RESPONSIBLE_PERSON=request.POST['RESPONSIBLE_PERSON'],OWNER_ALL=OWNER_ALL,OWNER_PROJECT_ID=OWNER_PROJECT_ID,CREATE_USER_ID=request.session['userId'] ,CREATE_USER_NAME=request.session['username'],
                      )
        module.save()

        response_data['resultCode']='0000'
        response_data['resultDesc']='Success'
    except Exception, ex:

        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode']='0001'
        response_data['resultDesc']=ex.__str__()
    log.info('module_add end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


def module_select(request):
    log.info('module_select start')
    log.info("request: "+str(request))
    response_data = {}
    try:
        # 本页第一条数据下标
        offset = request.GET.get('offset')
        # 每页数量
        limit = request.GET.get('limit')
        # 排序asc，desc
        order= ''
        if request.GET.get('order')=='desc':
            order='-'
        ordername='id'
        if request.GET.get('ordername'):
            ordername= str(request.GET.get('ordername'))
        ordername=ordername.replace('fields.','')
        orderBy=order+ordername
        name = ''
        description = ''
        systemId=0
        if request.GET.get("name"):
            name = request.GET.get("name")
        if request.GET.get("description"):
            description = request.GET.get("description")
        if  int(request.GET.get("systemId"))==0:
            t_module_List = T_MODULE.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description).order_by(orderBy)
        else:
            systemId = request.GET.get("systemId")
            t_module_List = T_MODULE.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description).filter(SYSTEM_ID_id=int(systemId)).order_by(orderBy)

        total=len(t_module_List)

        list = t_module_List[int(offset):int(offset) + int(limit)]


        # [5:10]这是查找从下标5到下标10之间的数据，不包括10。
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '查询成功！'
        # 序列码 serializers.serialize，且ensure_ascii=False防止乱码
        response_data['rows'] = serializers.serialize('json', list, ensure_ascii=False,use_natural_keys=True)
        response_data['total'] = total
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()

    log.info('module_select end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


def module_delete(request):
    log.info('module_delete start')
    log.info("request: "+str(request))
    form = {}
    if request.POST:
        form['id'] = request.POST['id']
        log.info("form:"+str(form))
        if not T_MODULE.objects.check_id(request,form['id']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"模块没有使用权限！"}))
    # 根据id删除的数据
    response_data = {}
    try:
        log.info('delete id:'+form['id'] )
        module = T_MODULE.objects.get(id=form['id'])
        module.delete()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '删除成功'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    log.info('module_delete end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

def module_unwarp(request):
    log.info('module_unwarp start')
    log.info("request: "+str(request))
    form = {}
    if request.POST:
        form['id'] = request.POST['id']
        log.info("form:"+str(form))
        if not T_MODULE.objects.check_id(request,form['id']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"模块没有使用权限！"}))
    # 根据id删除的数据
    response_data = {}
    try:
        log.info('unwarp id:'+form['id'] )
        module = T_MODULE.objects.get(id=form['id'])
        module.SYSTEM_ID_id=None
        module.save()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '解绑成功'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    log.info('module_unwarp end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

# 更新任务 根据id  更新

def module_update(request):
    log.info('module_update start')
    log.info("request: "+str(request))
    response_data = {}
    form={}
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    try:
        if not T_MODULE.objects.check_id(request,request.POST['id']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"模块没有使用权限！"}))
        if not T_SYSTEM.objects.check_id(request,request.POST['SYSTEM_ID']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"系统没有使用权限！"}))

        if T_MODULE.objects.filter(NAME=request.POST['NAME'],SYSTEM_ID_id=int(request.POST['SYSTEM_ID'])).exists():
            if not T_MODULE.objects.get(NAME=request.POST['NAME'],SYSTEM_ID_id=int(request.POST['SYSTEM_ID'])).id == int(request.POST['id']):
                response_data['resultCode']='0001'
                response_data['resultDesc']='系统中该模块已经存在，名称不能重复！'
                return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

        if request.POST['OWNER']=='onlyOne':
            OWNER_ID=request.session['userId']
            OWNER_NAME=request.session['username']
        elif request.POST['OWNER']=='all':
            OWNER_ALL=True
        else:
            if not T_PROJECT.objects.check_id(request,request.POST['OWNER']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"项目组没有使用权限！"}))
            OWNER_PROJECT_ID=request.POST['OWNER']

        module = T_MODULE.objects.get(id=request.POST['id'])
        module.NAME = request.POST['NAME']
        module.DESCRIPTION =request.POST['DESCRIPTION']
        module.SYSTEM_ID_id = int(request.POST['SYSTEM_ID']) if not int(request.POST['SYSTEM_ID'])==0 else None
        module.RESPONSIBLE_PERSON =request.POST['RESPONSIBLE_PERSON']
        module.OWNER_NAME = OWNER_NAME
        module.OWNER_ID = OWNER_ID
        module.OWNER_PROJECT_ID = OWNER_PROJECT_ID
        module.OWNER_ALL = OWNER_ALL
        module.MODIFY_USER_ID=request.session['userId']
        module.save()
        log.info('update module:'+str(model_to_dict(module)))

        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '修改成功！'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] =e.__str__()
    log.info('module_update end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


def init_module_select(request):
    log.info('init_module_select start')
    module=T_MODULE.objects.check_own(request)
    moduleList = serializers.serialize('json', module, ensure_ascii=False)
    true = True
    false=False
    null = None
    #log.info('userList：'+userList)
    log.info('init_module_select end')
    return HttpResponse(json.dumps({'moduleList': eval(moduleList)}))