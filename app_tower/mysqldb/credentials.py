#!/usr/bin/env python
# -*- coding:utf8 -*-
from django.forms.models import model_to_dict
from app_tower.models import T_LOGIN_CREDENTIALS,T_PROJECT
from django.http import HttpRequest,HttpResponse
from django.http import JsonResponse

from django.core import serializers
import traceback

# des 加密
from app_tower.utils import desJiami
import json
import logging
log = logging.getLogger("credentials") # 为loggers中定义的名称
from authority.permission import PermissionVerify
from vega.settings import SECRET_KEY

#description:添加登录凭证
#params: request.POST {"credentials_name":"test","credentials_desc":"test","credentials_owner":"onlyOne","credentials_type":"machine","credentials_loginUser":"root","credentials_password":"1qaz!QAZ",
#"credentials_privilege":"su","privilege_password":"1qaz!QAZ"}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def credentials_add(request):

    log.info('credentials_add start')
    log.info("request: "+str(request))
    form = {}
    response_data={}
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    try:
        if request.POST:
            form['name'] = request.POST['credentials_name']
            form['description'] = request.POST['credentials_desc']
            form['owner'] = request.POST['credentials_owner']
            form['type'] = request.POST['credentials_type']
            form['loginUser'] = request.POST['credentials_loginUser']
            form['loginPassword'] = request.POST['credentials_password']
            form['privilege'] = request.POST['credentials_privilege']
            form['privilege_password'] = request.POST['privilege_password']
            # DES 加密
            d = desJiami.DES()
            # 用提升密码来作为  DES 的key
            d.input_key(SECRET_KEY)
            # 加密
            log.info(form['loginPassword'])
            form['loginPassword'] = d.encode(str(request.POST['credentials_password']))
            form['privilege_password'] = d.encode(str(request.POST['privilege_password']))
            # d.decode(传入字符串来解密)
        log.info("form:"+str(form))
        if form['owner']=='onlyOne':
            OWNER_ID=request.session['userId']
            OWNER_NAME=request.session['username']
        elif form['owner']=='all':
            OWNER_ALL=True
        else:
            if not T_PROJECT.objects.check_id(request,form['owner']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"项目组没有使用权限！"}))
            OWNER_PROJECT_ID=form['owner']
        if T_LOGIN_CREDENTIALS.objects.filter(NAME=form['name']):
            response_data['resultCode']='0001'
            response_data['resultDesc']='NAME已经存在，名称不能重复！'
            return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")
        credentials = T_LOGIN_CREDENTIALS(NAME=form['name'],DESCRIPTION=form['description'],OWNER_ID=OWNER_ID,OWNER_NAME=OWNER_NAME,OWNER_PROJECT_ID=OWNER_PROJECT_ID,OWNER_ALL=OWNER_ALL,TYPE=form['type'],LOGIN_USER=form['loginUser'],LOGIN_PWD=form['loginPassword']
        ,CREATE_USER_ID=request.session['userId'] ,CREATE_USER_NAME=request.session['username'],PRIVILEGE_NAME=form['privilege'],PRIVILEGE_PWD=form['privilege_password'])
        credentials.save()
        log.info('credentials add :'+str(model_to_dict(credentials)))
        response_data['resultCode']='0000'
        response_data['resultDesc']='Success'
    except Exception, ex:
        print Exception, ex
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode']='0001'
        response_data['resultDesc']=ex.__str__()
    log.info('credentials_add end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#description:查询登录凭证
#params: request.GET {"limit":5,"offset":0,"order":"asc","ordername":"id","name":"","description":""}
#return: {"resultCode":"","resultDesc":"","rows":"","total":""}
@PermissionVerify()
def credentials_select(request):

    log.info('credentials_select start')
    log.info("request: "+str(request))
    response_data={}
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
        ordername=ordername.replace('fields.','')
        orderBy=order+ordername
        #排序
        name=''
        description=''
        if request.GET.get("name"):
            name=request.GET.get("name")
        if request.GET.get("description"):
            description=request.GET.get("description")
        credentialsList=T_LOGIN_CREDENTIALS.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description).order_by(orderBy)
        total=len(credentialsList)
        log.info('total:'+str(total))
        list = credentialsList[int(offset):int(offset)+int(limit)]
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = 'SUCCESS'
        #序列码 serializers.serialize，且ensure_ascii=False防止乱码
        response_data['rows'] = serializers.serialize('json', list,ensure_ascii=False,)
        response_data['total'] = total
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()

    log.info('response_data:'+str(response_data))
    log.info("credentials_select end")
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#description:删除登录凭证
#params: request.POST {"id":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def credentials_delete(request):
    log.info('credentials_delete start')
    log.info("request: "+str(request))
    form = {}
    if request.POST:
        form['id'] = request.POST['id']
        log.info("id:"+form['id'])
    # 根据id删除的数据
    response_data = {}
    if not T_LOGIN_CREDENTIALS.objects.check_id(request,form['id']):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"登录凭证没有使用权限！"}))
    credentials = T_LOGIN_CREDENTIALS.objects.get(id=form['id'])
    try:
        credentials.delete()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '删除成功！'
    except Exception,ex:
        traceback.print_exc()
        log.error(ex)
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = '已被使用，禁止删除！'
    log.info('credentials_delete end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:修改登录凭证
#params: request.POST {"id":credentials.id,"name":"test1","description":"test1","type":"machine","loginUser":"root","loginPassword":"2wsx@WSX","privilege":"su",
#    "privilegePassword":"2wsx@WSX","owner":"onlyOne"}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def credentials_update(request):
    log.info('credentials_update start')
    log.info("request: "+str(request))
    response_data = {}
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    if not T_LOGIN_CREDENTIALS.objects.check_id(request,request.POST['id']):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"登录凭证没有使用权限！"}))
    if T_LOGIN_CREDENTIALS.objects.filter(NAME=request.POST['name']).exists():
        if not T_LOGIN_CREDENTIALS.objects.get(NAME=request.POST['name']).id == int(request.POST['id']):
            response_data['resultCode']='0001'
            response_data['resultDesc']='NAME已经存在，名称不能重复！'
            return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")
    try:
        if request.POST:
            credentials = T_LOGIN_CREDENTIALS.objects.get(id=int(request.POST['id']))
            credentials.NAME = request.POST['name']
            credentials.DESCRIPTION = request.POST['description']

            credentials.TYPE = request.POST['type']
            credentials.LOGIN_USER = request.POST['loginUser']
            d = desJiami.DES()
            # 用提升密码来作为  DES 的key
            d.input_key(SECRET_KEY)
            # 加密
            credentials.LOGIN_PWD =credentials.LOGIN_PWD if credentials.LOGIN_PWD==str(request.POST['loginPassword']) else  d.encode(str(request.POST['loginPassword']))
            credentials.PRIVILEGE_NAME = request.POST['privilege']
            credentials.PRIVILEGE_PWD =credentials.PRIVILEGE_PWD if credentials.PRIVILEGE_PWD==str(request.POST['privilegePassword']) else d.encode(str(request.POST['privilegePassword']))
            credentials.LAST_MODIFY_USER_ID=request.session['userId']
            if request.POST['owner']=='onlyOne':
                OWNER_ID=request.session['userId']
                OWNER_NAME=request.session['username']
            elif request.POST['owner']=='all':
                OWNER_ALL=True
            else:
                if not T_PROJECT.objects.check_id(request,request.POST['owner']):
                    return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"项目组没有使用权限！"}))
                OWNER_PROJECT_ID=request.POST['owner']
            credentials.OWNER_ID=OWNER_ID
            credentials.OWNER_NAME=OWNER_NAME
            credentials.OWNER_ALL=OWNER_ALL
            credentials.OWNER_PROJECT_ID=OWNER_PROJECT_ID
            credentials.save()
            log.info(str(model_to_dict(credentials)))
            response_data['resultCode'] = '0000'
            response_data['resultDesc'] = '更新成功！'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    log.info('credentials_update end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")