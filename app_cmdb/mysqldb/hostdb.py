#!/usr/bin/env python
# -*- coding:utf8 -*-
from app_tower.models import T_HOST,T_PROJECT
from app_tower.models import T_SYSTEM
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from json import dumps
import json
import os
import traceback
# 写excel数据 (xls)   pyexcel_xls 以 OrderedDict 结构处理数据
from collections import OrderedDict
from pyexcel_xls import save_data
from django.core import serializers
from authority.permission import PermissionVerify
import logging
log = logging.getLogger("host")

#description:添加主机
#params: request.POST {"NAME":"10.200.86.172","DESCRIPTION":"test","VARIABLES":"","OWNER":"onlyOne","MACHINE_TYPE":"1","MACHINE_ROOM":"1","MACHINE_POSITION":"1","CUTTER_NUMBER":"1","SN_NUMBER":"1",
# "OS":"1","PHYSICAL_MACHINE_TYPE":"1","NOTE":"1","SYSTEM_ID":system.id}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def host_add(request):
    log.info('host_add start')
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
        if T_HOST.objects.filter(NAME=request.POST['NAME']):
            response_data['resultCode']='0001'
            response_data['resultDesc']='NAME已经存在，名称不能重复！'
            return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

        host = T_HOST(NAME=request.POST['NAME'], DESCRIPTION=request.POST['DESCRIPTION'], VARIABLES=request.POST['VARIABLES'],OWNER_ID=OWNER_ID,OWNER_NAME=OWNER_NAME,OWNER_ALL=OWNER_ALL,OWNER_PROJECT_ID=OWNER_PROJECT_ID,CREATE_USER_ID=request.session['userId'] ,CREATE_USER_NAME=request.session['username'],
                      MACHINE_TYPE=request.POST['MACHINE_TYPE'],MACHINE_ROOM=request.POST['MACHINE_ROOM'],MACHINE_POSITION=request.POST['MACHINE_POSITION'],CUTTER_NUMBER=request.POST['CUTTER_NUMBER'],SN_NUMBER=request.POST['SN_NUMBER'],OS=request.POST['OS'],
                      PHYSICAL_MACHINE_TYPE=request.POST['PHYSICAL_MACHINE_TYPE'],NOTE=request.POST['NOTE'],SYSTEM_ID=T_SYSTEM.objects.get(id=request.POST['SYSTEM_ID']))
        host.save()

        response_data['resultCode']='0000'
        response_data['resultDesc']='Success'
    except Exception, ex:

        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode']='0001'
        response_data['resultDesc']=ex.__str__()
    log.info('host_add end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#description:查询主机列表
#params: request.GET {"limit":5,"offset":0,"order":"asc","ordername":"id","systemId":"0"}
#return: {"resultCode":"","resultDesc":"","rows":"","total":""}
@PermissionVerify()
def host_select(request):
    log.info('host_select start')
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
            t_host_List = T_HOST.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description).order_by(orderBy)
        else:
            systemId = request.GET.get("systemId")
            t_host_List = T_HOST.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description).filter(SYSTEM_ID_id=int(systemId)).order_by(orderBy)

        total=len(t_host_List)
        list = t_host_List[int(offset):int(offset) + int(limit)]

        for l in list:
            if l.SYSTEM_ID==None:
                l.ARGS1=""
            else:
                l.ARGS1=l.SYSTEM_ID.NAME

        # [5:10]这是查找从下标5到下标10之间的数据，不包括10。
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '查询成功！'
        # 序列码 serializers.serialize，且ensure_ascii=False防止乱码
        response_data['rows'] = serializers.serialize('json', list, ensure_ascii=False)
        response_data['total'] = total
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()

    log.info('host_select end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#description:删除主机
#params: request.POST {"id":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def host_delete(request):
    log.info('host_delete start')
    log.info("request: "+str(request))
    form = {}
    if request.POST:
        form['id'] = request.POST['id']
        log.info("form:"+str(form))
        if not T_HOST.objects.check_id(request,form['id']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机没有使用权限！"}))
    # 根据id删除的数据
    response_data = {}
    try:
        log.info('delete id:'+form['id'] )
        host = T_HOST.objects.get(id=form['id'])
        host.delete()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '删除成功'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    log.info('host_delete end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:修改主机
#params: request.POST {"id":"","NAME":"jzyuan","DESCRIPTION":"test","VARIABLES":"","OWNER":"onlyOne","MACHINE_TYPE":"1","MACHINE_ROOM":"1","MACHINE_POSITION":"1","CUTTER_NUMBER":"1","SN_NUMBER":"1",
# "OS":"1","PHYSICAL_MACHINE_TYPE":"1","NOTE":"1","SYSTEM_ID":system.id}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def host_update(request):
    log.info('host_update start')
    log.info("request: "+str(request))
    response_data = {}
    form={}
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    try:
        if not T_HOST.objects.check_id(request,request.POST['id']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机没有使用权限！"}))
        if not T_SYSTEM.objects.check_id(request,request.POST['SYSTEM_ID']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"系统没有使用权限！"}))
        if T_HOST.objects.filter(NAME=request.POST['NAME']).exists():
            if not T_HOST.objects.get(NAME=request.POST['NAME']).id == int(request.POST['id']):
                response_data['resultCode']='0001'
                response_data['resultDesc']='NAME已经存在，名称不能重复！'
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

        host = T_HOST.objects.get(id=request.POST['id'])
        host.SYSTEM_ID =T_SYSTEM.objects.get(id=request.POST['SYSTEM_ID'])
        host.NAME = request.POST['NAME']
        host.DESCRIPTION =request.POST['DESCRIPTION']
        host.MACHINE_TYPE =request.POST['MACHINE_TYPE']
        host.MACHINE_ROOM =request.POST['MACHINE_ROOM']
        host.MACHINE_POSITION =request.POST['MACHINE_POSITION']
        host.CUTTER_NUMBER =request.POST['CUTTER_NUMBER']
        host.SN_NUMBER =request.POST['SN_NUMBER']
        host.OS =request.POST['OS']
        host.NOTE =request.POST['NOTE']
        host.PHYSICAL_MACHINE_TYPE =request.POST['PHYSICAL_MACHINE_TYPE']
        host.VARIABLES =request.POST['VARIABLES']
        host.OWNER_NAME = OWNER_NAME
        host.OWNER_ID = OWNER_ID
        host.OWNER_PROJECT_ID = OWNER_PROJECT_ID
        host.OWNER_ALL = OWNER_ALL
        host.MODIFY_USER_ID=request.session['userId']
        host.save()
        log.info('update host:'+str(model_to_dict(host)))

        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '修改成功！'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] =e.__str__()
    log.info('host_update end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:导出主机，程序列表
#params: request.POST {"name":"","description":"","systemId":""}
#return: {"resultCode":"","resultDesc":"","filepath":""}
#导出系统组件程序主机关系xlsx文件
@PermissionVerify()
def host_export(request):
    response_data = {}
    log.info('host_export start')
    try:
        # 查询
        name = ''
        description = ''
        systemId=0
        if request.POST["name"]:
            name = request.POST["name"]
        if request.POST["description"]:
            description = request.POST["description"]
        if request.POST["systemId"]:
            systemId = request.POST["systemId"]
        if int(systemId)==0:
            t_host_List = T_HOST.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description)
        else:
            t_host_List = T_HOST.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description).filter(SYSTEM_ID_id=int(systemId))

        # 写Excel数据, xls格式
        data = OrderedDict()
        charts={}
        # sheet表的数据

        row_1_data = [u"IP地址",u"描述",u"部署程序",u"程序描述",u"程序负责人",u"默认监听端口",u"默认部署目录",u"默认部署账号",u"定时脚本任务",u"日志输出",u"备注",u"数据备份路径",u"数据文件路径",u"所属组件（模块）",u"组件描述",u"组件负责人",u"所属系统", u"系统描述",u"责任公司"]  # 每一行的数据
        row_2_data=[u"IP地址",u"描述",u"所属系统",u"机器类型",u"机房",u"机架位置",u"刀框编号",u"SN好",u"OS",u"物理机配置类型",u"变量",u"备注"]
        # 遍历  逐条添加数据
        sheet_1 = []
        # 添加表头
        sheet_1.append(row_1_data)

        for host in t_host_List:

            if  host.t_software_set.count()==0:

                row_data=[host.NAME,host.DESCRIPTION]
                sheet_1.append(row_data)
            else:
                for software in host.t_software_set.all():

                      module=  software.MODULE_ID
                      system=module.SYSTEM_ID
                      row_data=[host.NAME,host.DESCRIPTION,software.NAME,software.DESCRIPTION,software.RESPONSIBLE_PERSON,software.LISTEN_PORT
                            ,software.DEPLOY_DIR,software.DEPLOY_ACCOUNT,software.TIMER_SCRIPT,software.LOG_EXPORT,software.NOTE,software.DATA_BACKUPPATH,software.DATA_FILEPATH,
                                  module.NAME,module.DESCRIPTION,module.RESPONSIBLE_PERSON,system.NAME,system.DESCRIPTION,system.COMPANY]
                      sheet_1.append(row_data)

        log.info(sheet_1)
        charts[u"系统主机-程序信息列表"]=sheet_1
        sheet_2 = []
        # 添加表头
        sheet_2.append(row_2_data)
        for host in t_host_List:

            if host.SYSTEM_ID_id==None:

                sheet_2.append([host.NAME,host.DESCRIPTION,"",host.MACHINE_TYPE,host.MACHINE_ROOM,host.MACHINE_POSITION,host.CUTTER_NUMBER,host.SN_NUMBER,host.OS,host.PHYSICAL_MACHINE_TYPE,host.VARIABLES,host.NOTE])
            else:

                sheet_2.append([host.NAME,host.DESCRIPTION,host.SYSTEM_ID.NAME,host.MACHINE_TYPE,host.MACHINE_ROOM,host.MACHINE_POSITION,host.CUTTER_NUMBER,host.SN_NUMBER,host.OS,host.PHYSICAL_MACHINE_TYPE,host.VARIABLES,host.NOTE])
        charts[u"主机信息列表"]=sheet_2
        # 添加sheet表
        log.info(charts)
        data.update(charts)
        log.info(data)
        exportRoot = str(os.getcwd()) + "/export/host.xls"
        # 保存成xls文件
        save_data(exportRoot, data)
        response_data['resultCode'] = '0000'
        response_data['filepath'] =exportRoot
        # response_data['filename'] ="write.xls"
        response_data['resultDesc'] = 'Success'
    except Exception, ex:
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = ex.__str__()
    log.info('host_export end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


def host_download(request):
    response_data={}
    form={}
    log.info('host_download start')
    form["filepath"]=request.GET['filepath']
    form["filename"]="host"
    form["filetype"]=".xls"
    # 下载文件
    def readFile(fn, buf_size=262144):  # 大文件下载，设定缓存大小
        f = open(fn, "rb")
        while True:  # 循环读取
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    response = HttpResponse(readFile(form["filepath"]),
                            content_type='APPLICATION/OCTET-STREAM')  # 设定文件头，这种设定可以让任意文件都能正确下载，而且已知文本文件不是本地打开
    response['Content-Disposition'] = 'attachment; filename=' + form["filename"] + form["filetype"] # 设定传输给客户端的文件名称
    response['Content-Length'] = os.path.getsize(form["filepath"])  # 传输给客户端的文件大小
    log.info('host_download end')
    # 导出成功之后   删除服务器上的文件
    os.remove(form["filepath"])
    return response