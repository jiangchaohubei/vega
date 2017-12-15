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
log = logging.getLogger("system")


def system_add(request):
    log.info('system_add start')
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
        if T_SYSTEM.objects.filter(NAME=request.POST['NAME']):
            response_data['resultCode']='0001'
            response_data['resultDesc']='系统已经存在，名称不能重复！'
            return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

        system = T_SYSTEM(NAME=request.POST['NAME'], DESCRIPTION=request.POST['DESCRIPTION'], COMPANY=request.POST['COMPANY'],OWNER_ALL=OWNER_ALL,OWNER_PROJECT_ID=OWNER_PROJECT_ID,CREATE_USER_ID=request.session['userId'] ,CREATE_USER_NAME=request.session['username'],
                      )
        system.save()

        response_data['resultCode']='0000'
        response_data['resultDesc']='Success'
    except Exception, ex:

        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode']='0001'
        response_data['resultDesc']=ex.__str__()
    log.info('system_add end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


def system_select(request):
    log.info('system_select start')
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
        company=''
        if request.GET.get("name"):
            name = request.GET.get("name")
        if request.GET.get("description"):
            description = request.GET.get("description")
        if request.GET.get("company"):
            company = request.GET.get("company")
        # 排序字段
        # ordername= request.GET.get('ordername')
        # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM     Test.objects.filter(name="runoob").order_by("id")
        t_system_List = T_SYSTEM.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description).filter(COMPANY__contains=company).order_by(orderBy)
        total=len(t_system_List)

        list = t_system_List[int(offset):int(offset) + int(limit)]

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

    log.info('system_select end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


def system_delete(request):
    log.info('system_delete start')
    log.info("request: "+str(request))
    form = {}
    if request.POST:
        form['id'] = request.POST['id']
        log.info("form:"+str(form))
        if not T_SYSTEM.objects.check_id(request,form['id']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"系统没有使用权限！"}))
    # 根据id删除的数据
    response_data = {}
    try:
        log.info('delete id:'+form['id'] )
        system = T_SYSTEM.objects.get(id=form['id'])
        system.delete()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '删除成功'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    log.info('system_delete end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


# 更新任务 根据id  更新

def system_update(request):
    log.info('system_update start')
    log.info("request: "+str(request))
    response_data = {}
    form={}
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    try:
        if not T_SYSTEM.objects.check_id(request,request.POST['id']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"系统没有使用权限！"}))
        if T_SYSTEM.objects.filter(NAME=request.POST['NAME']).exists():
            if not T_SYSTEM.objects.get(NAME=request.POST['NAME']).id == int(request.POST['id']):
                response_data['resultCode']='0001'
                response_data['resultDesc']='系统已经存在，名称不能重复！'
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

        system = T_SYSTEM.objects.get(id=request.POST['id'])
        system.NAME = request.POST['NAME']
        system.DESCRIPTION =request.POST['DESCRIPTION']
        system.COMPANY =request.POST['COMPANY']
        system.OWNER_NAME = OWNER_NAME
        system.OWNER_ID = OWNER_ID
        system.OWNER_PROJECT_ID = OWNER_PROJECT_ID
        system.OWNER_ALL = OWNER_ALL
        system.MODIFY_USER_ID=request.session['userId']
        system.save()
        log.info('update system:'+str(model_to_dict(system)))

        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '修改成功！'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] =e.__str__()
    log.info('system_update end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

def init_system_select(request):
    log.info('init_system_select start')
    system=T_SYSTEM.objects.check_own(request)
    systemList = serializers.serialize('json', system, ensure_ascii=False)
    true = True
    false=False
    null = None
    #log.info('userList：'+userList)
    log.info('init_system_select end')
    return HttpResponse(json.dumps({'systemList': eval(systemList)}))

#导出系统组件程序主机关系xlsx文件
def system_export(request):
    response_data = {}
    log.info('system_export start')
    try:
        # 查询
        name = ''
        description = ''
        company=''
        if request.POST["name"]:
            name = request.POST["name"]
        if request.POST["description"]:
            description = request.POST["description"]
        if request.POST["company"]:
            company = request.POST["company"]
        # 排序字段
        # ordername= request.GET.get('ordername')
        # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM     Test.objects.filter(name="runoob").order_by("id")
        log.info(name)
        t_system_List = T_SYSTEM.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description).filter(COMPANY__contains=company)

        # 写Excel数据, xls格式
        data = OrderedDict()
        charts={}
        # sheet表的数据

        row_1_data = [u"系统名称", u"系统描述",u"责任公司",u"组件（模块）名称",u"组件描述",u"组件负责人",u"部署程序",u"程序描述",u"程序负责人",u"默认监听端口",u"默认部署目录",u"默认部署账号",u"定时脚本任务",u"日志输出",u"备注",u"数据备份路径",u"数据文件路径",u"IP地址"]  # 每一行的数据

        # 遍历  逐条添加数据
        for system in t_system_List:
            sheet_1 = []
            # 添加表头
            sheet_1.append(row_1_data)
            if  system.SYSTEM_ID_T_MODULE.count()==0:
                row_data=[system.NAME,system.DESCRIPTION,system.COMPANY]
                sheet_1.append(row_data)
            else:
                for module in system.SYSTEM_ID_T_MODULE.all():
                    if  module.MODULE_ID_T_SOFTWARE.count()==0:
                        row_data=[system.NAME,system.DESCRIPTION,system.COMPANY,module.NAME,module.DESCRIPTION,module.RESPONSIBLE_PERSON]
                        sheet_1.append(row_data)
                    else:
                        for software in module.MODULE_ID_T_SOFTWARE.all():
                            if  software.HOSTS.count()==0:
                                row_data=[system.NAME,system.DESCRIPTION,system.COMPANY,module.NAME,module.DESCRIPTION,module.RESPONSIBLE_PERSON,software.NAME,software.DESCRIPTION,software.RESPONSIBLE_PERSON,software.LISTEN_PORT
                                    ,software.DEPLOY_DIR,software.DEPLOY_ACCOUNT,software.TIMER_SCRIPT,software.LOG_EXPORT,software.NOTE,software.DATA_BACKUPPATH,software.DATA_FILEPATH]

                                sheet_1.append(row_data)
                            else:
                                for host in software.HOSTS.all():
                                    row_data=[system.NAME,system.DESCRIPTION,system.COMPANY,module.NAME,module.DESCRIPTION,module.RESPONSIBLE_PERSON,software.NAME,software.DESCRIPTION,software.RESPONSIBLE_PERSON,software.LISTEN_PORT
                                              ,software.DEPLOY_DIR,software.DEPLOY_ACCOUNT,software.TIMER_SCRIPT,software.LOG_EXPORT,software.NOTE,software.DATA_BACKUPPATH,software.DATA_FILEPATH,host.NAME]

                                    sheet_1.append(row_data)


            charts[system.NAME]=sheet_1

        # 添加sheet表
        log.info(charts)
        data.update(charts)
        log.info(data)
        exportRoot = str(os.getcwd()) + "/export/system.xls"
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
    log.info('system_export end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


def system_download(request):
    response_data={}
    form={}
    log.info('system_download start')
    form["filepath"]=request.GET['filepath']
    form["filename"]="system"
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
    log.info('system_download end')
    # 导出成功之后   删除服务器上的文件
    os.remove(form["filepath"])
    return response