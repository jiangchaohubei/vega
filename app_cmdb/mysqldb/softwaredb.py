#!/usr/bin/env python
# -*- coding:utf8 -*-
from app_tower.models import T_HOST,T_PROJECT
from app_tower.models import T_SYSTEM,T_MODULE,T_SOFTWARE,T_SOFTWARE_HOST_ID
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from json import dumps
import json
import traceback

from django.core import serializers
from authority.permission import PermissionVerify
import logging
log = logging.getLogger("software")

#description:添加程序
#params: request.POST {"NAME":"test","DESCRIPTION":"test","RESPONSIBLE_PERSON":"1","OWNER":"onlyOne","MODULE_ID":module.id,"LISTEN_PORT":"1",
#"DEPLOY_DIR":"1","DEPLOY_ACCOUNT":"1","TIMER_SCRIPT":"1","LOG_EXPORT":"1","NOTE":"1","DATA_BACKUPPATH":"1","DATA_FILEPATH":"1"}
#return: {"resultCode":"","resultDesc":""}
def software_add(request):
    log.info('software_add start')
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
        if not T_MODULE.objects.check_id(request,request.POST['MODULE_ID']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"模块没有使用权限！"}))

        if T_SOFTWARE.objects.filter(NAME=request.POST['NAME'],MODULE_ID_id=int(request.POST['MODULE_ID'])).exists():
            response_data['resultCode']='0001'
            response_data['resultDesc']='模块中该程序已经存在，名称不能重复！'
            return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

        software = T_SOFTWARE(NAME=request.POST['NAME'], DESCRIPTION=request.POST['DESCRIPTION'],MODULE_ID=T_MODULE.objects.get(id=request.POST['MODULE_ID']),RESPONSIBLE_PERSON=request.POST['RESPONSIBLE_PERSON'],OWNER_ALL=OWNER_ALL,OWNER_PROJECT_ID=OWNER_PROJECT_ID,CREATE_USER_ID=request.session['userId'] ,CREATE_USER_NAME=request.session['username'],
                    LISTEN_PORT=request.POST['LISTEN_PORT'] if request.POST['LISTEN_PORT'] else 22,DEPLOY_DIR=request.POST['DEPLOY_DIR'],DEPLOY_ACCOUNT=request.POST['DEPLOY_ACCOUNT'],TIMER_SCRIPT=request.POST['TIMER_SCRIPT'],LOG_EXPORT=request.POST['LOG_EXPORT'],
                              NOTE=request.POST['NOTE'],DATA_BACKUPPATH=request.POST['DATA_BACKUPPATH'],DATA_FILEPATH=request.POST['DATA_FILEPATH'],)
        software.save()

        response_data['resultCode']='0000'
        response_data['resultDesc']='Success'
    except Exception, ex:

        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode']='0001'
        response_data['resultDesc']=ex.__str__()
    log.info('software_add end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:查询程序
#params: request.GET {"offset":"1","limit":"5","order":"asc","ordername":"id","name":"","description":"","moduleId":"","systemId":""}
#return: {"resultCode":"","resultDesc":"","rows":"","total":""}
def software_select(request):
    log.info('software_select start')
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
        moduleId=0
        systemId=0
        t_software_List=[]
        if request.GET.get("name"):
            name = request.GET.get("name")
        if request.GET.get("description"):
            description = request.GET.get("description")
        if  int(request.GET.get("moduleId"))==0:
            if int(request.GET.get("systemId"))==0:
                t_software_List = T_SOFTWARE.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description).order_by(orderBy)
            else:
                systemId = request.GET.get("systemId")
                modules=T_SYSTEM.objects.get(id=int(systemId)).SYSTEM_ID_T_MODULE.all()
                for m in modules:
                    for s in m.MODULE_ID_T_SOFTWARE.all():
                        t_software_List.append(s)
        else:
            moduleId = request.GET.get("moduleId")
            t_software_List = T_SOFTWARE.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description).filter(MODULE_ID_id=int(moduleId)).order_by(orderBy)

        total=len(t_software_List)

        list = t_software_List[int(offset):int(offset) + int(limit)]

        for l in list:
            l.ARGS1=l.MODULE_ID.NAME

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

    log.info('software_select end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#description:删除程序
#params: request.POST   {"id":""}
#return: {"resultCode":"","resultDesc":""}
def software_delete(request):
    log.info('software_delete start')
    log.info("request: "+str(request))
    form = {}
    if request.POST:
        form['id'] = request.POST['id']
        log.info("form:"+str(form))
        if not T_SOFTWARE.objects.check_id(request,form['id']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"程序没有使用权限！"}))
    # 根据id删除的数据
    response_data = {}
    try:
        log.info('delete id:'+form['id'] )
        software = T_SOFTWARE.objects.get(id=form['id'])
        software.delete()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '删除成功'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    log.info('software_delete end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:修改程序
#params: request.POST {"id":"","NAME":"test","DESCRIPTION":"test","RESPONSIBLE_PERSON":"1","OWNER":"onlyOne","MODULE_ID":module.id,"LISTEN_PORT":"1",
#"DEPLOY_DIR":"1","DEPLOY_ACCOUNT":"1","TIMER_SCRIPT":"1","LOG_EXPORT":"1","NOTE":"1","DATA_BACKUPPATH":"1","DATA_FILEPATH":"1"}
#return: {"resultCode":"","resultDesc":""}
def software_update(request):
    log.info('software_update start')
    log.info("request: "+str(request))
    response_data = {}
    form={}
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    try:
        if not T_SOFTWARE.objects.check_id(request,request.POST['id']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"程序没有使用权限！"}))
        if not T_MODULE.objects.check_id(request,request.POST['MODULE_ID']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"模块没有使用权限！"}))
        if T_SOFTWARE.objects.filter(NAME=request.POST['NAME'],MODULE_ID_id=int(request.POST['MODULE_ID'])).exists():
            if not T_SOFTWARE.objects.get(NAME=request.POST['NAME'],MODULE_ID_id=int(request.POST['MODULE_ID'])).id == int(request.POST['id']):
                response_data['resultCode']='0001'
                response_data['resultDesc']='模块中该程序已经存在，名称不能重复！'
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

        software = T_SOFTWARE.objects.get(id=request.POST['id'])
        software.NAME = request.POST['NAME']
        software.DESCRIPTION =request.POST['DESCRIPTION']
        software.MODULE_ID_id =int(request.POST['MODULE_ID']) if not int(request.POST['MODULE_ID'])==0 else None
        software.RESPONSIBLE_PERSON =request.POST['RESPONSIBLE_PERSON']
        software.LISTEN_PORT =request.POST['LISTEN_PORT']
        software.DEPLOY_DIR =request.POST['DEPLOY_DIR']
        software.DEPLOY_ACCOUNT =request.POST['DEPLOY_ACCOUNT']
        software.TIMER_SCRIPT =request.POST['TIMER_SCRIPT']
        software.LOG_EXPORT =request.POST['LOG_EXPORT']
        software.NOTE =request.POST['NOTE']
        software.DATA_BACKUPPATH =request.POST['DATA_BACKUPPATH']
        software.DATA_FILEPATH =request.POST['DATA_FILEPATH']

        software.OWNER_NAME = OWNER_NAME
        software.OWNER_ID = OWNER_ID
        software.OWNER_PROJECT_ID = OWNER_PROJECT_ID
        software.OWNER_ALL = OWNER_ALL
        software.MODIFY_USER_ID=request.session['userId']
        software.save()
        log.info('update software:'+str(model_to_dict(software)))

        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '修改成功！'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] =e.__str__()
    log.info('software_update end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


def init_system_module_select(request):
    log.info('init_system_module_select start')
    modulesown=[]
    systemId=request.POST['systemId']
    if int(systemId)==0:
        modulesown=T_MODULE.objects.check_own(request)
    else:
        system=T_SYSTEM.objects.get(id=systemId)
        modules=system.SYSTEM_ID_T_MODULE.all()
        for m in modules:
            if T_MODULE.objects.check_id(request,m.id):
                modulesown.append(m)
    moduleList = serializers.serialize('json', modulesown, ensure_ascii=False)
    true = True
    false=False
    null = None
    #log.info('userList：'+userList)
    log.info('init_system_module_select end')
    return HttpResponse(json.dumps({'moduleList': eval(moduleList)}))

#description:绑定主机和程序
#params: request.POST {"id":"","hostList":"[]"}
#return: {"resultCode":"","resultDesc":"","errorHost":[]}
def host_add(request):
    log.info('host_add start')
    log.info("request: "+str(request))
    form = {}
    response_data={}
    try:
        if request.POST:
            form['id'] = request.POST['id']
            if not T_SOFTWARE.objects.check_id(request,form['id']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"程序没有使用权限！"}))
            form['hostList'] = request.POST['hostList']

            log.info("form:"+str(form))
        software = T_SOFTWARE.objects.get(id=form['id'])
        system=software.MODULE_ID.SYSTEM_ID
        error_host=[]
        for h in eval(form['hostList']):

            host=T_HOST.objects.get(NAME=h)
            if host.SYSTEM_ID_id==system.id :
                software_host,create = T_SOFTWARE_HOST_ID.objects.get_or_create(SOFTWARE_ID=software, HOST_ID=host)
                software_host.save()
            else:
                error_host.append(host.NAME)

        response_data['resultCode']='0000'
        response_data['resultDesc']='Success'
        response_data['errorHost']=error_host
    except Exception, ex:
        print Exception, ex
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode']='0001'
        response_data['resultDesc']=ex.__str__()
    log.info('host_add end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:查询程序所拥有的所有主机
#params: request.GET {"offset":"1","limit":"5","order":"asc","ordername":"","id":"software.id"}
#return: {"resultCode":"","resultDesc":"","rows":"","total":""}
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
        id = request.GET.get('id')
        # 排序字段
        # ordername= request.GET.get('ordername')
        sofaware = T_SOFTWARE.objects.get(id=id)
        ##多对多的查询##
        hostlist = sofaware.HOSTS.all().order_by(orderBy)
        total = len(hostlist)
        list = hostlist[int(offset):int(offset) + int(limit)]
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

#description:解绑程序所拥有的主机
#params: request.POST {"id":"host.id","softwareId":"softwareId"}
#return: {"resultCode":"","resultDesc":"",}
def host_delete(request):
    log.info('host_delete start')
    log.info("request: "+str(request))
    form = {}
    response_data = {}
    try:
        if request.POST:
            form['id'] = request.POST['id']
            if not T_HOST.objects.check_id(request,form['id']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机没有使用权限！"}))
            form['softwareId'] = request.POST['softwareId']
            if not T_SOFTWARE.objects.check_id(request,form['softwareId']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"程序没有使用权限！"}))
        # 删除id=1的数据
        host = T_HOST.objects.get(id=form['id'])
        group = T_SOFTWARE.objects.get(id=form['softwareId'])
        T_SOFTWARE_HOST_ID.objects.filter(SOFTWARE_ID=group,HOST_ID=host).delete()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '解绑成功！'
    except Exception, ex:
        print Exception, ex
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = ex.__str__()
    log.info('host_delete end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

def init_cmdb_system(request):
    log.info('init_cmdb_system end')
    response_data = {}
    try:
        softwareId=request.POST['softwareId']
        if not T_SOFTWARE.objects.check_id(request,int(softwareId)):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"程序没有使用权限！"}))
        system=T_SOFTWARE.objects.get(id=int(softwareId)).MODULE_ID.SYSTEM_ID

        response_data['resultCode']='0000'
        response_data['resultDesc']='查询成功'
        response_data['systemId']= system.id
        response_data['systemName']= system.NAME
    except Exception, ex:
        print Exception, ex
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = ex.__str__()
    log.info('init_cmdb_system end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")