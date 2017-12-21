#!/usr/bin/env python
# -*- coding:utf8 -*-
from app_tower.models import T_HOST,T_PROJECT
from app_tower.models import T_SYSTEM,T_MODULE,T_SOFTWARE,T_VERSION
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from json import dumps
import json
import traceback
import os
from django.core import serializers
from authority.permission import PermissionVerify
import logging
log = logging.getLogger("version")

#description:添加版本
#params: request.POST {"softwareId":"softwareId","NAME":"1.0","DESCRIPTION":"","INSTALL_PATH":""}
#return: {"resultCode":"","resultDesc":""}
def version_add(request):
    log.info('version_add start')
    log.info("request: "+str(request))
    response_data={}
    try:
        softwareId=request.POST['softwareId']
        if not T_SOFTWARE.objects.check_id(request,softwareId):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"程序没有使用权限！"}))
        NAME=request.POST['NAME']
        DESCRIPTION=request.POST['DESCRIPTION']
        INSTALL_PATH=request.POST['INSTALL_PATH']


        if T_VERSION.objects.filter(NAME=NAME,SOFTWARE_ID_id=int(softwareId)).exists():
            response_data['resultCode']='0001'
            response_data['resultDesc']='请填写不存在的版本号！'
            return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")
        #创建存储文件夹
        software=T_SOFTWARE.objects.get(id=int(softwareId))
        #rote_path="C:\Users\PC\Desktop\\versions"
        rote_path="/opt/versions"
        if not os.path.exists(rote_path):
            os.makedirs(rote_path)
        systemName=software.MODULE_ID.SYSTEM_ID.NAME
        rote_path=rote_path+"/"+systemName
        if not os.path.exists(rote_path):
            os.makedirs(rote_path)
        moduleName=software.MODULE_ID.NAME
        rote_path=rote_path+"/"+moduleName
        if not os.path.exists(rote_path):
            os.makedirs(rote_path)
        softwareName=software.NAME
        rote_path=rote_path+"/"+softwareName
        if not os.path.exists(rote_path):
            os.makedirs(rote_path)
        rote_path=rote_path+"/"+NAME
        if not os.path.exists(rote_path):
            os.makedirs(rote_path)
        file =request.FILES.get("file", None)
        PACKAGE_PATH=""
        if file==None:
            PACKAGE_PATH=""
        else:
            PACKAGE_PATH=rote_path+"/"+file.name    ##根目录(/opt/versions)+所属系统名+模块名+程序名+版本号+文件名
            # 分块写入文件
            fo=open(PACKAGE_PATH,"wb")
            for chunk in file.chunks():
                fo.write(chunk)

        version = T_VERSION(NAME=request.POST['NAME'], DESCRIPTION=DESCRIPTION,SOFTWARE_ID=software,INSTALL_PATH=INSTALL_PATH,PACKAGE_PATH=PACKAGE_PATH,OWNER_ID=software.OWNER_ID,OWNER_NAME=software.OWNER_NAME,
                             OWNER_ALL=software.OWNER_ALL,OWNER_PROJECT_ID=software.OWNER_PROJECT_ID,CREATE_USER_ID=request.session['userId'] ,CREATE_USER_NAME=request.session['username'],
                              )
        version.save()

        response_data['resultCode']='0000'
        response_data['resultDesc']='Success'
    except Exception, ex:

        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode']='0001'
        response_data['resultDesc']=ex.__str__()
    log.info('version_add end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#description:查询版本
#params: request.GET {"offset":"1","limit":"5","order":"asc","ordername":"id","name":"","description":"","softwareId":"softwareId"}
#return: {"resultCode":"","resultDesc":"","rows":"","total":""}
def version_select(request):
    log.info('version_select start')
    log.info("request: "+str(request))
    response_data = {}
    try:
        # 本页第一条数据下标
        offset = request.GET.get('offset')
        # 每页数量
        limit = request.GET.get('limit')
        # 排序asc，desc
        order= '-'
        if request.GET.get('order')=='desc':
            order='-'
        elif request.GET.get('order')=='asc':
            order=''
        ordername='id'
        if request.GET.get('ordername'):
            ordername= str(request.GET.get('ordername'))
        ordername=ordername.replace('fields.','')
        orderBy=order+ordername
        name = ''
        description = ''
        if request.GET.get("name"):
            name = request.GET.get("name")
        if request.GET.get("description"):
            description = request.GET.get("description")
        if request.GET.get("softwareId"):
            softwareId = request.GET.get("softwareId")
        # 排序字段
        # ordername= request.GET.get('ordername')
        # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM     Test.objects.filter(name="runoob").order_by("id")
        t_version_List = T_VERSION.objects.check_own(request).filter(NAME__contains=name,SOFTWARE_ID_id=softwareId).filter(DESCRIPTION__contains=description).order_by(orderBy)
        total=len(t_version_List)

        list = t_version_List[int(offset):int(offset) + int(limit)]
        for l in list:
            l.ARGS1=l.SOFTWARE_ID.NAME

        # [5:10]这是查找从下标5到下标10之间的数据，不包括10。
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '查询成功！'
        # 序列码 serializers.serialize，且ensure_ascii=False防止乱码
        response_data['rows'] = serializers.serialize('json', list, ensure_ascii=False,use_natural_keys=False)

        response_data['total'] = total
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()

    log.info('version_select end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#description:删除版本
#params: request.POST   {"id":"versionId"}
#return: {"resultCode":"","resultDesc":""}
def version_delete(request):
    log.info('version_delete start')
    log.info("request: "+str(request))
    form = {}
    if request.POST:
        form['id'] = request.POST['id']
        log.info("form:"+str(form))
        if not T_VERSION.objects.check_id(request,form['id']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"版本没有使用权限！"}))
    # 根据id删除的数据
    response_data = {}
    try:
        log.info('delete id:'+form['id'] )
        version = T_VERSION.objects.get(id=form['id'])
        version.delete()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '删除成功'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    log.info('version_delete end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


