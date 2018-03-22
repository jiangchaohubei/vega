#!/usr/bin/env python
# -*- coding:utf8 -*-
from app_tower.models import T_TOOL,T_TOOL_INPUT,T_TOOL_OUTPUT,T_TOOLTYPE,T_PROJECT,T_TOOL_User_ID,User,T_LOGIN_CREDENTIALS,T_TOOL_EVENT,IMG,T_TOOL_EVENT_COUNT
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from json import dumps
import json
import tempfile
import traceback
import os
import time
from app_tower.utils import dateutil
from django.db import  transaction
from django.core import serializers
from app_tower.tasks import run_tool_yaml,run_tool_shell
from celery.task.control import revoke
from celery.result import AsyncResult
from django.utils.timezone import now, timedelta
from authority.permission import PermissionVerify
from app_tower.signals import tool_passaudit,tool_create
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import logging
log = logging.getLogger("working")

#初始化作业平台
def working_init(request):
    log.info('working_init start')
    toolType=T_TOOLTYPE.objects.all()
    toolTypeList = serializers.serialize('json', toolType, ensure_ascii=False)
    tool=User.objects.get(id=request.session['userId']).tools.all().filter(AUDIT_STATUS=1)
    toolList = serializers.serialize('json', tool, ensure_ascii=False)
    true = True
    false=False
    null = None
    #log.info('userList：'+userList)
    log.info('working_init end')
    return HttpResponse(json.dumps({'resultCode':'0000','toolType': eval(toolTypeList),'tools': eval(toolList)}))

#初始化工具商店
def toolshop_init(request):
    log.info('toolshop_init start')

    tool_0 = T_TOOL.objects.all().filter(AUDIT_STATUS=0)
    tool_1 = T_TOOL.objects.all().filter(AUDIT_STATUS=1)
    tool_2 = T_TOOL.objects.all().filter(AUDIT_STATUS=2)
    project=T_PROJECT.objects.check_own(request)

    true = True
    null = None
    false=False

    for t in tool_0:
        t.ARGS1=t.TOOLTYPE_ID.NAME
    for t in tool_1:
        t.ARGS1=t.TOOLTYPE_ID.NAME
    for t in tool_2:
        t.ARGS1=t.TOOLTYPE_ID.NAME
    toolList0 = serializers.serialize('json', tool_0, ensure_ascii=False)
    toolList1 = serializers.serialize('json', tool_1, ensure_ascii=False)
    toolList2 = serializers.serialize('json', tool_2, ensure_ascii=False)
    projectList = serializers.serialize('json', project, ensure_ascii=False)
    #已经导入的工具
    tools=User.objects.get(id=request.session['userId']).tools.all().filter(AUDIT_STATUS=1)
    for t in tools:
        t.ARGS1=t.TOOLTYPE_ID.NAME
    toolimported = serializers.serialize('json', tools, ensure_ascii=False)

    true = True
    false=False
    null = None
    #log.info('userList：'+userList)
    log.info('toolshop_init end')
    return HttpResponse(json.dumps({'resultCode':'0000','toolimported':eval(toolimported),'tools_audited': eval(toolList1),'tools_notaudited': eval(toolList0),'tools_failaudited': eval(toolList2),'projectList': eval(projectList)}))

#初始化工具创建页面
def toolcreate_init(request):
    log.info('toolcreate_init start')

    tooltype=T_TOOLTYPE.objects.all()
    tooltypeList = serializers.serialize('json', tooltype, ensure_ascii=False)
    project=T_PROJECT.objects.check_own(request)
    projectList = serializers.serialize('json', project, ensure_ascii=False)
    imgs=IMG.objects.all()
    imgList = serializers.serialize('json', imgs, ensure_ascii=False)

    true = True
    false=False
    null = None
    #log.info('userList：'+userList)
    log.info('toolcreate_init end')
    return HttpResponse(json.dumps({'resultCode':'0000','tooltypeList': eval(tooltypeList),'projectList': eval(projectList),'imgList': eval(imgList)}))

#初始化工具创建页面
def icons_init(request):
    log.info('icons_init start')
    imgs=IMG.objects.all()
    imgList = serializers.serialize('json', imgs, ensure_ascii=False)

    true = True
    false=False
    null = None
    #log.info('userList：'+userList)
    log.info('icons_init end')
    return HttpResponse(json.dumps({'resultCode':'0000','imgList': eval(imgList)}))


#初始化工具明细
def toolDetail_init(request):
    log.info('toolDetail_init start')
    toolid=request.POST['toolid']
    tool=T_TOOL.objects.get(id=int(toolid))
    tool.AUDIT_TIME=json.dumps(tool.AUDIT_TIME, cls=dateutil.CJsonEncoder)
    tool.ARGS1=tool.TOOLTYPE_ID.NAME
    if tool.OWNER_ALL:
        tool.ARGS2=u'所有人'
    elif tool.OWNER_PROJECT_ID:
        tool.ARGS2=T_PROJECT.objects.get(id=int(tool.OWNER_PROJECT_ID)).NAME+U'(项目组)'
    else:
        tool.ARGS2=tool.OWNER_NAME
    print  tool.ARGS2
    toolinput=tool.T_TOOL_ID_T_TOOL_INPUT.all()
    tooloutput=tool.T_TOOL_ID_T_TOOL_OUTPUT.all()
    toolinputList = serializers.serialize('json', toolinput, ensure_ascii=False)
    tooloutputList = serializers.serialize('json', tooloutput, ensure_ascii=False)
    true = True
    false=False
    null = None
    #log.info('userList：'+userList)
    log.info('toolDetail_init end')
    print str(model_to_dict(tool))
    return HttpResponse(json.dumps({'resultCode':'0000','tool':model_to_dict(tool),'toolinput': eval(toolinputList),'tooloutput': eval(tooloutputList)}))

#初始化编辑
def tooledit_init(request):
    log.info('tooledit_init start')
    toolid=request.POST['toolid']
    tool=T_TOOL.objects.get(id=int(toolid))
    tool.AUDIT_TIME=json.dumps(tool.AUDIT_TIME, cls=dateutil.CJsonEncoder)
    tool.ARGS1=tool.TOOLTYPE_ID.NAME
    if tool.OWNER_ALL:
        tool.ARGS2=u'所有人'
    elif tool.OWNER_PROJECT_ID:
        tool.ARGS2=T_PROJECT.objects.get(id=int(tool.OWNER_PROJECT_ID)).NAME+U'(项目组)'
    else:
        tool.ARGS2=tool.OWNER_NAME
    print  tool.ARGS2
    toolinput=tool.T_TOOL_ID_T_TOOL_INPUT.all()
    tooloutput=tool.T_TOOL_ID_T_TOOL_OUTPUT.all()
    toolinputList = serializers.serialize('json', toolinput, ensure_ascii=False)
    tooloutputList = serializers.serialize('json', tooloutput, ensure_ascii=False)
    tooltype=T_TOOLTYPE.objects.all()
    tooltypeList = serializers.serialize('json', tooltype, ensure_ascii=False)
    project=T_PROJECT.objects.check_own(request)
    projectList = serializers.serialize('json', project, ensure_ascii=False)
    imgs=IMG.objects.all()
    imgList = serializers.serialize('json', imgs, ensure_ascii=False)
    true = True
    false=False
    null = None
    #log.info('userList：'+userList)
    log.info('tooledit_init end')
    print str(model_to_dict(tool))
    return HttpResponse(json.dumps({'resultCode':'0000','tool':model_to_dict(tool),'toolinput': eval(toolinputList),'tooloutput': eval(tooloutputList),'tooltypeList': eval(tooltypeList),'projectList': eval(projectList),'imgList': eval(imgList)}))

def get_event(request):
    toolEventId=request.POST['toolEventId']
    t_tool_event_count=T_TOOL_EVENT_COUNT.objects.filter(TOOL_EVENT_ID=toolEventId)
    eventList= serializers.serialize('json', t_tool_event_count,ensure_ascii=False)
    true = True
    false=False
    null = None
    return HttpResponse(json.dumps({'eventList':eval(eventList)}))

#初始化历史任务
def toolEvent_init(request):
    log.info('toolEvent_init start')
    toolEventId=request.POST['toolEventId']
    toolEvent=T_TOOL_EVENT.objects.get(id=int(toolEventId))
    toolEvent.ARGS1=toolEvent.TOOL_ID.NAME
    toolEvent.START_TIME=json.dumps(toolEvent.START_TIME, cls=dateutil.CJsonEncoder)
    toolEvent.FINISH_TIME=json.dumps(toolEvent.FINISH_TIME, cls=dateutil.CJsonEncoder)
    true = True
    false=False
    null = None

    log.info('toolEvent_init end')
    print str(model_to_dict(toolEvent))
    return HttpResponse(json.dumps({'resultCode':'0000','toolEvent':model_to_dict(toolEvent)}))

#初始化执行工具页面
def runTool_init(request):
    log.info('toolDetail_init start')
    toolid=request.POST['toolid']
    tool=T_TOOL.objects.get(id=int(toolid))
    tool.AUDIT_TIME=json.dumps(tool.AUDIT_TIME, cls=dateutil.CJsonEncoder)
    tool.ARGS1=tool.TOOLTYPE_ID.NAME
    if tool.OWNER_ALL:
        tool.ARGS2=u'所有人'
    elif tool.OWNER_PROJECT_ID:
        tool.ARGS2=T_PROJECT.objects.get(id=int(tool.OWNER_PROJECT_ID)).NAME+U'(项目组)'
    else:
        tool.ARGS2=tool.OWNER_NAME
    print  tool.ARGS2
    toolinput=tool.T_TOOL_ID_T_TOOL_INPUT.all()
    tooloutput=tool.T_TOOL_ID_T_TOOL_OUTPUT.all()
    toolinputList = serializers.serialize('json', toolinput, ensure_ascii=False)
    tooloutputList = serializers.serialize('json', tooloutput, ensure_ascii=False)
    credentials=T_LOGIN_CREDENTIALS.objects.check_own(request)
    credentialsList=serializers.serialize('json', credentials, ensure_ascii=False)
    true = True
    false=False
    null = None
    #log.info('userList：'+userList)
    log.info('toolDetail_init end')
    print str(model_to_dict(tool))
    return HttpResponse(json.dumps({'resultCode':'0000','tool':model_to_dict(tool),'toolinput': eval(toolinputList),'tooloutput': eval(tooloutputList),'credentialsList': eval(credentialsList)}))

def icon_upload(request):
    log.info('icon_upload start')
    log.info("request: "+str(request))
    response_data={}
    try:
        new_img = IMG(
            IMG=request.FILES.get('itemImagers'),
            NAME = request.FILES.get('itemImagers').name
        )
        new_img.save()
        response_data['resultCode']='0000'
        response_data['resultDesc']=request.FILES.get('itemImagers').name+'上传成功！'
    except Exception, ex:
        print Exception, ex
        traceback.print_exc()
        log.error(ex.__str__())
        log.error(traceback.print_exc())
        response_data['resultCode']='0001'
        response_data['resultDesc']=ex.__str__()
    log.info('icon_upload end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#description:添加工具
#params: request.POST {"name":"","type":"","language":"","scriptCode":"","des":"","inputParam":"[]","outputParam":"[]","owner":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def tool_add(request):
    log.info('tool_add start')
    log.info("request: "+str(request))
    form = {}
    response_data={}
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    try:
        if request.POST:
            form['name'] = request.POST['name']
            form['type'] = request.POST['type']
            form['icon'] = request.POST['icon']
            form['dangerlevel'] = request.POST['dangerlevel']
            form['language'] = request.POST['language']
            form['scriptCode'] = request.POST['scriptCode']
            form['des'] = request.POST['des']
            form['inputParam'] = request.POST['inputParam']
            form['outputParam'] = request.POST['outputParam']
            form['OWNER'] = request.POST['owner']
            log.info("form:"+str(form))
        if form['OWNER']=='onlyOne':
            OWNER_ID=request.session['userId']
            OWNER_NAME=request.session['username']
        elif form['OWNER']=='all':
            OWNER_ALL=True
        else:
            if not T_PROJECT.objects.check_id(request,form['OWNER']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"项目组没有使用权限！"}))
            OWNER_PROJECT_ID=form['OWNER']
        if T_TOOL.objects.filter(NAME=form['name']):
            response_data['resultCode']='0001'
            response_data['resultDesc']='NAME已经存在，名称不能重复！'
            return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")
        with transaction.atomic():
            tooltype,create=T_TOOLTYPE.objects.get_or_create(NAME=form['type'])
            tooltype.save()
            if form['language']=='shell':
                form['language']=0
            elif form['language']=='python':
                form['language']=1
            else:
                form['language']=2
            tool = T_TOOL(NAME=form['name'], DESCRIPTION=form['des'], TOOLTYPE_ID=tooltype,SCRIPT_LANGUAGE=form['language'],SCRIPT_CODE=form['scriptCode'],ICON=form['icon'],DANGER_LEVEL=form['dangerlevel'],
                          OWNER_ID=OWNER_ID, OWNER_NAME=OWNER_NAME, OWNER_PROJECT_ID=OWNER_PROJECT_ID, OWNER_ALL=OWNER_ALL,
                          CREATE_USER_ID=request.session['userId'],CREATE_USER_NAME=request.session['username'],
                          )
            tool.save()
            #批量添加输入输出参数
            false=False
            true=True
            inputParam_list=list()
            for item in eval(form['inputParam']):
                if not str(item)=='0':

                    inputparam=T_TOOL_INPUT(NAME=item['name'], DESCRIPTION=item['des'],DEFAULT=item['def'],ISREQUIRED=item['isrequired'],TYPE=int(item['type']),T_TOOL_ID=tool,
                                            OWNER_ID=OWNER_ID, OWNER_NAME=OWNER_NAME, OWNER_PROJECT_ID=OWNER_PROJECT_ID, OWNER_ALL=OWNER_ALL,
                                            CREATE_USER_ID=request.session['userId'],CREATE_USER_NAME=request.session['username'])
                    inputParam_list.append(inputparam)
            T_TOOL_INPUT.objects.bulk_create(inputParam_list)

            outputParam_list=list()
            for item in eval(form['outputParam']):
                if not str(item)=='0':
                    outputparam=T_TOOL_OUTPUT(NAME=item['name'], DESCRIPTION=item['des'],TYPE=int(item['type']),T_TOOL_ID=tool,
                                              OWNER_ID=OWNER_ID, OWNER_NAME=OWNER_NAME, OWNER_PROJECT_ID=OWNER_PROJECT_ID, OWNER_ALL=OWNER_ALL,
                                              CREATE_USER_ID=request.session['userId'],CREATE_USER_NAME=request.session['username'])
                    outputParam_list.append(outputparam)
            T_TOOL_OUTPUT.objects.bulk_create(outputParam_list)
            #触发信号
            tool_create.send(sender='tool_add',toolname=tool.NAME)

        response_data['resultCode']='0000'
        response_data['resultDesc']='Success'
    except Exception, ex:
        print Exception, ex
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode']='0001'
        response_data['resultDesc']=ex.__str__()
    log.info('project_add end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#description:编辑工具
#params: request.POST {"toolid":"","name":"","type":"","language":"","scriptCode":"","des":"","inputParam":"[]","outputParam":"[]","owner":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def tool_update(request):
    log.info('tool_update start')
    log.info("request: "+str(request))
    form = {}
    response_data={}
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    try:
        if request.POST:
            form['toolid'] = request.POST['toolid']
            if not T_TOOL.objects.check_id(request,int(form['toolid'])):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"工具没有使用权限！"}))
            form['name'] = request.POST['name']
            form['type'] = request.POST['type']
            form['icon'] = request.POST['icon']
            form['dangerlevel'] = request.POST['dangerlevel']
            form['language'] = request.POST['language']
            form['scriptCode'] = request.POST['scriptCode']
            form['des'] = request.POST['des']
            form['inputParam'] = request.POST['inputParam']
            form['outputParam'] = request.POST['outputParam']
            form['OWNER'] = request.POST['owner']
            log.info("form:"+str(form))
        if form['OWNER']=='onlyOne':
            OWNER_ID=request.session['userId']
            OWNER_NAME=request.session['username']
        elif form['OWNER']=='all':
            OWNER_ALL=True
        else:
            if not T_PROJECT.objects.check_id(request,form['OWNER']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"项目组没有使用权限！"}))
            OWNER_PROJECT_ID=form['OWNER']
        # if T_TOOL.objects.filter(NAME=form['name']):
        #     response_data['resultCode']='0001'
        #     response_data['resultDesc']='NAME已经存在，名称不能重复！'
        #     return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")
        with transaction.atomic():
            tooltype,create=T_TOOLTYPE.objects.get_or_create(NAME=form['type'])
            tooltype.save()
            if form['language']=='shell':
                form['language']=0
            elif form['language']=='python':
                form['language']=1
            else:
                form['language']=2

            T_TOOL.objects.filter(id=int(form['toolid'])).update(NAME=form['name'], DESCRIPTION=form['des'], TOOLTYPE_ID=tooltype,SCRIPT_LANGUAGE=form['language'],SCRIPT_CODE=form['scriptCode'],ICON=form['icon'],DANGER_LEVEL=form['dangerlevel'],
                                                                 OWNER_ID=OWNER_ID, OWNER_NAME=OWNER_NAME, OWNER_PROJECT_ID=OWNER_PROJECT_ID, OWNER_ALL=OWNER_ALL,
                                                                 MODIFY_USER_ID=request.session['userId'],AUDIT_STATUS=0,AUDIT_USER_ID=request.session['userId'],
                                                                 AUDIT_USER_NAME=request.session['username'],AUDIT_REASON=None,AUDIT_TIME=None)

            #批量添加输入输出参数
            false=False
            true=True
            inputParam_list=list()
            T_TOOL_INPUT.objects.filter(T_TOOL_ID_id=int(form['toolid'])).delete()
            for item in eval(form['inputParam']):
                if not str(item)=='0':

                    inputparam=T_TOOL_INPUT(NAME=item['name'], DESCRIPTION=item['des'],DEFAULT=item['def'],ISREQUIRED=item['isrequired'],TYPE=int(item['type']),T_TOOL_ID_id=int(form['toolid']),
                                            OWNER_ID=OWNER_ID, OWNER_NAME=OWNER_NAME, OWNER_PROJECT_ID=OWNER_PROJECT_ID, OWNER_ALL=OWNER_ALL,
                                            CREATE_USER_ID=request.session['userId'],CREATE_USER_NAME=request.session['username'])
                    inputParam_list.append(inputparam)
            T_TOOL_INPUT.objects.bulk_create(inputParam_list)

            outputParam_list=list()
            T_TOOL_OUTPUT.objects.filter(T_TOOL_ID_id=int(form['toolid'])).delete()
            for item in eval(form['outputParam']):
                if not str(item)=='0':
                    outputparam=T_TOOL_OUTPUT(NAME=item['name'], DESCRIPTION=item['des'],TYPE=int(item['type']),T_TOOL_ID_id=int(form['toolid']),
                                              OWNER_ID=OWNER_ID, OWNER_NAME=OWNER_NAME, OWNER_PROJECT_ID=OWNER_PROJECT_ID, OWNER_ALL=OWNER_ALL,
                                              CREATE_USER_ID=request.session['userId'],CREATE_USER_NAME=request.session['username'])
                    outputParam_list.append(outputparam)
            T_TOOL_OUTPUT.objects.bulk_create(outputParam_list)

            #触发信号
            tool_create.send(sender='tool_update',toolname=form['name'])

        response_data['resultCode']='0000'
        response_data['resultDesc']='Success'
    except Exception, ex:
        print Exception, ex
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode']='0001'
        response_data['resultDesc']=ex.__str__()
    log.info('tool_update end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#description:删除工具
#params: request.POST {"toolid":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def tool_delete(request):

    log.info("tool_delete start")
    log.info("request: "+str(request))
    form = {}

    if request.POST:
        form['toolid'] = request.POST['toolid']
        log.info("id:"+str(form))
    if not T_TOOL.objects.check_id(request,form['toolid']):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"工具没有删除权限！"}))
    # 删除id的数据
    tool = T_TOOL.objects.get(id=form['toolid'])
    response_data = {}
    try:
        tool.delete()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '删除成功！'
    except Exception,ex:
        print Exception,ex
        traceback.print_exc()
        log.error(ex)
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = '已被使用，禁止删除！'
    log.info("tool_delete end")
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:查询工具
#params: request.GET {"limit":5,"offset":0,"order":"asc","ordername":"id","name":"","description":""}
#return: {"resultCode":"","resultDesc":"","rows":"","total":""}
@PermissionVerify()
def tool_select(request):

    log.info("tool_select start")
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
        auditStatus=1
        if request.GET.get("name"):
            name=request.GET.get("name")
        if request.GET.get("description"):
            description=request.GET.get("description")
        if request.GET.get("auditStatus"):
            auditStatus=int(request.GET.get("auditStatus"))

        # 排序字段
        # ordername= request.GET.get('ordername')
        # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM     Test.objects.filter(name="runoob").order_by("id")
        toolList = T_TOOL.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description).filter(AUDIT_STATUS=auditStatus).order_by(orderBy)
        total=len(toolList)
        list = toolList[int(offset):int(offset)+int(limit)]
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
    log.info("tool_select end")
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:查询历史任务
#params: request.GET {"limit":5,"offset":0,"order":"asc","ordername":"id","name":"","description":""}
#return: {"resultCode":"","resultDesc":"","rows":"","total":""}
@PermissionVerify()
def history_select(request):

    log.info("history_select start")
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
        toolEventList=[]
        total=0
        if timeArea=='today':
            end = now().date()+timedelta(days=1)
            start =now().date()
            toolEventList = T_TOOL_EVENT.objects.check_own(request).filter(TOOL_ID__NAME__contains=name).filter(TOOL_ID__DESCRIPTION__contains=description).filter(CREATE_TIME__range=(start, end)).order_by(orderBy)
            total=len(toolEventList)
        elif timeArea=='week':
            end = now().date()+timedelta(days=1)
            start =now().date() - timedelta(days=7)
            toolEventList = T_TOOL_EVENT.objects.check_own(request).filter(TOOL_ID__NAME__contains=name).filter(TOOL_ID__DESCRIPTION__contains=description).filter(CREATE_TIME__range=(start, end)).order_by(orderBy)
            total=len(toolEventList)
        elif timeArea=='month':
            end = now().date()+timedelta(days=1)
            start =now().date() - timedelta(days=30)
            toolEventList = T_TOOL_EVENT.objects.check_own(request).filter(TOOL_ID__NAME__contains=name).filter(TOOL_ID__DESCRIPTION__contains=description).filter(CREATE_TIME__range=(start, end)).order_by(orderBy)
            total=len(toolEventList)
        else:
            toolEventList = T_TOOL_EVENT.objects.check_own(request).filter(TOOL_ID__NAME__contains=name).filter(TOOL_ID__DESCRIPTION__contains=description).filter(CREATE_TIME__range=(start, end)).order_by(orderBy)
            total=len(toolEventList)
        print end,start
        list = toolEventList[int(offset):int(offset)+int(limit)]
        #[5:10]这是查找从下标5到下标10之间的数据，不包括10。
        for l in list:
            l.ARGS1=l.TOOL_ID.NAME
            l.ARGS2=l.TOOL_ID.DESCRIPTION
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
    log.info("history_select end")
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:导入工具
#params: request.POST {"toolId":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def importTool(request):
    response_data={}
    try:
        toolId=request.POST['toolId']
        if not T_TOOL.objects.check_id(request,int(toolId)):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"工具没有使用权限！"}))
        tool=T_TOOL.objects.get(id=int(toolId))
        if not tool.AUDIT_STATUS == 1:
            return HttpResponse(json.dumps({"resultCode":"0001","resultDesc":"工具没有通过审核！"}))
        user=User.objects.get(id=int(request.session['userId']))
        tool_user,create=T_TOOL_User_ID.objects.get_or_create(TOOL_ID=tool,User_ID=user)
        tool_user.save()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '导入成功！'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:工具通过审核
#params: request.POST {"toolId":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def tool_audit(request):
    response_data={}
    try:
        toolid=request.POST['toolid']
        if not T_TOOL.objects.check_id(request,int(toolid)):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"工具没有使用权限！"}))
        auditStaus=request.POST['auditStaus']
        auditReason=request.POST['auditReason']
        tool=T_TOOL.objects.get(id=int(toolid))
        tool.AUDIT_STATUS=int(auditStaus)
        tool.AUDIT_USER_ID=request.session['userId']
        tool.AUDIT_USER_NAME=request.session['username']
        tool.AUDIT_REASON=auditReason
        tool.AUDIT_TIME=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        tool.save()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '审核成功！'

        tool_passaudit.send(sender='tool_audit',passaudit=True if int(auditStaus)==1 else False, toolname=tool.NAME)
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:移除工具
#params: request.POST {"toolId":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def removeTool(request):
    response_data={}
    try:
        toolId=request.POST['toolId']
        if not T_TOOL.objects.check_id(request,int(toolId)):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"工具没有使用权限！"}))
        user=User.objects.get(id=int(request.session['userId']))
        tool=T_TOOL.objects.get(id=int(toolId))
        T_TOOL_User_ID.objects.filter(TOOL_ID=tool,User_ID=user).delete()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '移除成功！'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#description:执行工具
#params: request.POST {"toolid":"","hostList":"[]","credentials":"","inputParams":"{}",}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def tool_run(request):
    response_data={}
    form={}
    try:
        if request.POST:
            form['toolid']=request.POST['toolid']
            if not T_TOOL.objects.check_id(request,int(form['toolid'])):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"工具没有使用权限！"}))
            form['credentialsId']=request.POST['credentials']
            form['hostList']=request.POST['hostList']
            form['inputParams']=request.POST['inputParams']
        print str(form)
        tool=T_TOOL.objects.get(id=int(form['toolid']))
        if not tool.AUDIT_STATUS == 1:
            return HttpResponse(json.dumps({"resultCode":"0001","resultDesc":"工具没有通过审核！"}))
        file=tempfile.NamedTemporaryFile(delete=False)  #临时文件记录日志
        tool_event=T_TOOL_EVENT(TOOL_ID=tool,CREDENTIALS_ID_id=int(form['credentialsId']),HOSTLIST=form['hostList'],INPUTPARAMS=form['inputParams'],CREATE_USER_ID=request.session['userId'],
                                CREATE_USER_NAME=request.session['username'],LOGFILE=file.name,STATUS='STARTED',OWNER_ID=tool.OWNER_ID,OWNER_NAME=tool.OWNER_NAME,OWNER_PROJECT_ID=tool.OWNER_PROJECT_ID,OWNER_ALL=tool.OWNER_ALL)
        tool_event.save()
        if tool.SCRIPT_LANGUAGE==2:   #yaml脚本
            jobTags=[]
            skipTags=[]
            extraVariable={}
            sudo=False
            su=False
            for param in eval(form['inputParams']):
                if param['type']=='5' and param['value']:
                    jobtagstr=param['value']+','
                    job_Tags=jobtagstr.split(',')
                    job_Tags.pop()
                    jobTags.extend(job_Tags)

                elif param['type']=='6' and param['value']:
                    skiptagstr=param['value']+','
                    skip_Tags=skiptagstr.split(',')
                    skip_Tags.pop()
                    skipTags.extend(skip_Tags)
                elif param['type']=='7' and param['value']:
                    extraVariable[param['name']]=param['value']
                elif param['type']=='8' and param['value']:
                    if  param['value']== '-s' :
                        sudo=True
                    elif  param['value']== '-S' :
                        su=True
            #临时playbook
            playbook=tempfile.NamedTemporaryFile(delete=False)
            fo = open(playbook.name, "w+")
            fo.write(tool.SCRIPT_CODE)
            fo.flush()
            fo.close()
            runtool = run_tool_yaml.delay(tool_event.id,int(form['credentialsId']),file.name,playbook.name,jobTags,skipTags,extraVariable,hostList=eval(request.POST['hostList']),sudo=sudo,su=su)
            taskid = runtool.task_id
            print taskid
            result = AsyncResult(taskid)
            log.info("STATUS:"+result.status)
            T_TOOL_EVENT.objects.filter(id=tool_event.id).update(STATUS=result.status,CELERY_TASK_ID=taskid)
            response_data['toolEventId'] = tool_event.id
            response_data['taskid'] = taskid
        elif tool.SCRIPT_LANGUAGE==0:   #shell脚本
            vars=""
            sudo=False
            su=False
            for param in eval(form['inputParams']):
                if param['type']=='0' and param['value']:
                    vars+=param['name']+"="+param['value']+"\n"
                elif param['type']=='8' and param['value']:
                    if  param['value']== '-s' :
                        sudo=True
                    elif  param['value']== '-S' :
                        su=True
            vars+=vars+tool.SCRIPT_CODE
            #临时script
            scriptPath=tempfile.NamedTemporaryFile(delete=False)
            fo = open(scriptPath.name, "w+")
            fo.write(vars)
            fo.flush()
            fo.close()
            runtool = run_tool_shell.delay(file.name,tool_event.id,int(form['credentialsId']),scriptPath.name,hostList=eval(request.POST['hostList']),sudo=sudo,su=su)
            taskid = runtool.task_id
            print taskid
            result = AsyncResult(taskid)
            log.info("STATUS:"+result.status)
            T_TOOL_EVENT.objects.filter(id=tool_event.id).update(STATUS=result.status,CELERY_TASK_ID=taskid)
            response_data['toolEventId'] = tool_event.id
            response_data['taskid'] = taskid


        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '成功！'
        response_data['runUser'] = request.session['username']
        response_data['toolName'] = tool.NAME
        response_data['logfile'] = file.name
        response_data['inputParams'] = form['inputParams']

    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")



#description:重新执行工具任务
#params: request.POST {"toolEventId":"",}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def tool_reRun(request):
    response_data={}
    form={}
    try:
        if request.POST:
            form['toolEventId']=request.POST['toolEventId']
            if not T_TOOL_EVENT.objects.check_id(request,int(form['toolEventId'])):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"没有使用权限！"}))

        print str(form)
        tool_event=T_TOOL_EVENT.objects.get(id=int(form['toolEventId']))
        tool=tool_event.TOOL_ID
        if not tool.AUDIT_STATUS == 1:
            return HttpResponse(json.dumps({"resultCode":"0001","resultDesc":"工具没有通过审核！"}))
        file=tempfile.NamedTemporaryFile(delete=False)  #临时文件记录日志
        tool_event2=T_TOOL_EVENT(TOOL_ID=tool,CREDENTIALS_ID_id=tool_event.CREDENTIALS_ID_id,HOSTLIST=tool_event.HOSTLIST,INPUTPARAMS=tool_event.INPUTPARAMS,CREATE_USER_ID=request.session['userId'],
                                 CREATE_USER_NAME=request.session['username'],LOGFILE=file.name,STATUS='STARTED',OWNER_ID=tool.OWNER_ID,OWNER_NAME=tool.OWNER_NAME,OWNER_PROJECT_ID=tool.OWNER_PROJECT_ID,OWNER_ALL=tool.OWNER_ALL)
        tool_event2.save()
        if tool.SCRIPT_LANGUAGE==2:   #yaml脚本
            jobTags=[]
            skipTags=[]
            extraVariable={}
            sudo=False
            su=False
            for param in eval(tool_event2.INPUTPARAMS):
                if param['type']=='5' and param['value']:
                    jobtagstr=param['value']+','
                    job_Tags=jobtagstr.split(',')
                    job_Tags.pop()
                    jobTags.extend(job_Tags)

                elif param['type']=='6' and param['value']:
                    skiptagstr=param['value']+','
                    skip_Tags=skiptagstr.split(',')
                    skip_Tags.pop()
                    skipTags.extend(skip_Tags)
                elif param['type']=='7' and param['value']:
                    extraVariable[param['name']]=param['value']
                elif param['type']=='8' and param['value']:
                    if  param['value']== '-s' :
                        sudo=True
                    elif  param['value']== '-S' :
                        su=True
            #临时playbook
            playbook=tempfile.NamedTemporaryFile(delete=False)
            fo = open(playbook.name, "w+")
            fo.write(tool.SCRIPT_CODE)
            fo.flush()
            fo.close()
            runtool = run_tool_yaml.delay(tool_event2.id,tool_event2.CREDENTIALS_ID_id,file.name,playbook.name,jobTags,skipTags,extraVariable,hostList=eval(tool_event2.HOSTLIST),sudo=sudo,su=su)
            taskid = runtool.task_id
            print taskid
            result = AsyncResult(taskid)
            log.info("STATUS:"+result.status)
            T_TOOL_EVENT.objects.filter(id=tool_event2.id).update(STATUS=result.status,CELERY_TASK_ID=taskid)
            response_data['toolEventId'] = tool_event2.id
            response_data['taskid'] = taskid
        elif tool.SCRIPT_LANGUAGE==0:   #shell脚本
            vars=""
            sudo=False
            su=False
            for param in eval(tool_event2.INPUTPARAMS):
                if param['type']=='0' and param['value']:
                    vars+=param['name']+"="+param['value']+"\n"
                elif param['type']=='8' and param['value']:
                    if  param['value']== '-s' :
                        sudo=True
                    elif  param['value']== '-S' :
                        su=True
            vars+=vars+tool.SCRIPT_CODE
            #临时script
            scriptPath=tempfile.NamedTemporaryFile(delete=False)
            fo = open(scriptPath.name, "w+")
            fo.write(vars)
            fo.flush()
            fo.close()
            runtool = run_tool_shell.delay(file.name,tool_event2.id,tool_event2.CREDENTIALS_ID_id,scriptPath.name,hostList=eval(tool_event2.HOSTLIST),sudo=sudo,su=su)
            taskid = runtool.task_id
            print taskid
            result = AsyncResult(taskid)
            log.info("STATUS:"+result.status)
            T_TOOL_EVENT.objects.filter(id=tool_event2.id).update(STATUS=result.status,CELERY_TASK_ID=taskid)
            response_data['toolEventId'] = tool_event2.id
            response_data['taskid'] = taskid


        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '成功！'
        response_data['runUser'] = request.session['username']
        response_data['toolName'] = tool.NAME
        response_data['logfile'] = file.name
        response_data['inputParams'] = tool_event2.INPUTPARAMS

    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#实时读取运行日志

def read_log(request):

    log.info('read_job_log start')
    log.info("request: "+str(request))
    response_data = {}
    try:
        seek=0
        if request.POST['seek']:
            seek=request.POST['seek']
        taskid=request.POST['taskid']
        logfile=request.POST['logfile']

        toolEventId=request.POST['toolEventId']


        tool_event=T_TOOL_EVENT.objects.get(id=int(toolEventId))
        state=tool_event.STATUS
        response_data['state']=state
        log.info('state:'+state)
        if not os.access(logfile, os.F_OK):
            #临时文件不存在
            response_data['log']=tool_event.LOGCONTENT
            response_data['seek']=0
        else :
            with open(logfile,'r') as f:
                f.seek(0)
                response_data['log'] =f.read()
                response_data['seek']=f.tell()


        response_data['toolEvent']={'startTime':json.dumps(tool_event.START_TIME, cls=dateutil.CJsonEncoder),
                                    'endTime':json.dumps(tool_event.FINISH_TIME, cls=dateutil.CJsonEncoder),'elapsed':tool_event.ELAPSED,}

        if response_data['state'] in ['SUCCESS','FAILURE','REVOKED']:
            response_data['read_flag']='False'
        else:
            response_data['read_flag']='True'

        response_data['resultCode']='0000'
        response_data['resultDesc']='成功'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode']='0001'
        response_data['resultDesc']=e.__str__()
    log.info('read_job_log end')
    return HttpResponse(json.dumps(response_data))

#停止执行工具

def stop_tool(request):
    log.info('stop_tool start')
    log.info("request: "+str(request))
    taskid=request.POST['taskid']
    toolEventId=request.POST['toolEventId']
    if not T_TOOL_EVENT.objects.check_id(request,toolEventId):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"没有使用权限！"}))
    revoke(taskid,terminate=True,signal='SIGKILL')
    result=AsyncResult(taskid)
    T_TOOL_EVENT.objects.filter(id=int(toolEventId)).update(STATUS='REVOKED',CANCEL_FLAG=True)
    log.info('stop_tool end status'+result.status)
    return HttpResponse(json.dumps({'success':'true','status':result.status}))


#导出工具

def tool_export(request):
    response_data = {}
    log.info('tool_export start')
    toolDetail={}
    try:

        if request.POST["toolid"]:
            toolid = request.POST["toolid"]
        tool=T_TOOL.objects.get(id=int(toolid))
        tool.AUDIT_TIME=json.dumps(tool.AUDIT_TIME, cls=dateutil.CJsonEncoder)
        toolinput=tool.T_TOOL_ID_T_TOOL_INPUT.all()
        tooloutput=tool.T_TOOL_ID_T_TOOL_OUTPUT.all()
        toolinputList = serializers.serialize('json', toolinput, ensure_ascii=False)
        tooloutputList = serializers.serialize('json', tooloutput, ensure_ascii=False)
        true = True
        false=False
        null = None
        toolDetail['tool']=model_to_dict(tool)
        toolDetail['type']=tool.TOOLTYPE_ID.NAME
        toolDetail['toolinput']=eval(toolinputList)
        toolDetail['tooloutput']=eval(tooloutputList)

        exporttime=str(time.time())
        exportRoot = str(os.getcwd()) + "/export/"+tool.NAME+exporttime+".json"
        fl=open(exportRoot, 'w')
        fl.write(json.dumps(toolDetail,ensure_ascii=False,indent=2))
        fl.close()

        response_data['resultCode'] = '0000'
        response_data['filepath'] =exportRoot
        response_data['filename'] =tool.NAME
        response_data['resultDesc'] = 'Success'
    except Exception, ex:
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = ex.__str__()
    log.info('tool_export end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


def tool_download(request):
    response_data={}
    form={}
    log.info('tool_download start')
    form["filepath"]=request.GET['filepath']
    form["filename"]=request.GET['filename'].encode('utf8')
    form["filetype"]=".json"
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

#导入工具
def leadinginTool(request):
    response_data = {}
    log.info("leadinginTool start")
    try:
        OWNER_ID=None
        OWNER_NAME=None
        OWNER_PROJECT_ID=None
        OWNER_ALL=False
        toolJson=""
        myFile = request.FILES.get("inputFile", None)  # 获取上传的文件，如果没有文件，则默认为None
        import_owner = request.POST['owner']
        if import_owner=='onlyOne':
            OWNER_ID=request.session['userId']
            OWNER_NAME=request.session['username']
        elif import_owner=='all':
            OWNER_ALL=True
        else:
            if not T_PROJECT.objects.check_id(request,int(import_owner)):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"项目组没有使用权限！"}))
            OWNER_PROJECT_ID=import_owner
        for chunk in myFile.chunks():
            toolJson+=chunk

        false=False
        null=None
        true=True
        toolDic=eval(toolJson)
        if T_TOOL.objects.filter(NAME=toolDic['tool']['NAME']).exists():
            response_data['resultCode']='0001'
            response_data['resultDesc']='工具名称已存在，名称不能重复！'
            return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")
        with transaction.atomic():
            tooltype,create=T_TOOLTYPE.objects.get_or_create(NAME=toolDic['type'])
            tooltype.save()

            tool = T_TOOL(NAME=toolDic['tool']['NAME'], DESCRIPTION=toolDic['tool']['DESCRIPTION'], TOOLTYPE_ID=tooltype,SCRIPT_LANGUAGE=toolDic['tool']['SCRIPT_LANGUAGE'],SCRIPT_CODE=toolDic['tool']['SCRIPT_CODE'],ICON=toolDic['tool']['ICON'],DANGER_LEVEL=toolDic['tool']['DANGER_LEVEL'],
                          OWNER_ID=OWNER_ID, OWNER_NAME=OWNER_NAME, OWNER_PROJECT_ID=OWNER_PROJECT_ID, OWNER_ALL=OWNER_ALL,
                          CREATE_USER_ID=request.session['userId'],CREATE_USER_NAME=request.session['username'],
                          )
            tool.save()
            #批量添加输入输出参数

            inputParam_list=list()
            for item in toolDic['toolinput']:
                if not str(item)=='0':

                    inputparam=T_TOOL_INPUT(NAME=item['fields']['NAME'], DESCRIPTION=item['fields']['DESCRIPTION'],DEFAULT=item['fields']['DEFAULT'],ISREQUIRED=item['fields']['ISREQUIRED'],TYPE=int(item['fields']['TYPE']),T_TOOL_ID=tool,
                                            OWNER_ID=OWNER_ID, OWNER_NAME=OWNER_NAME, OWNER_PROJECT_ID=OWNER_PROJECT_ID, OWNER_ALL=OWNER_ALL,
                                            CREATE_USER_ID=request.session['userId'],CREATE_USER_NAME=request.session['username'])
                    inputParam_list.append(inputparam)
            T_TOOL_INPUT.objects.bulk_create(inputParam_list)

            outputParam_list=list()
            for item in toolDic['tooloutput']:
                if not str(item)=='0':
                    outputparam=T_TOOL_OUTPUT(NAME=item['fields']['NAME'], DESCRIPTION=item['fields']['DESCRIPTION'],TYPE=int(item['fields']['TYPE']),T_TOOL_ID=tool,
                                              OWNER_ID=OWNER_ID, OWNER_NAME=OWNER_NAME, OWNER_PROJECT_ID=OWNER_PROJECT_ID, OWNER_ALL=OWNER_ALL,
                                              CREATE_USER_ID=request.session['userId'],CREATE_USER_NAME=request.session['username'])
                    outputParam_list.append(outputparam)
            T_TOOL_OUTPUT.objects.bulk_create(outputParam_list)
            #触发信号
            tool_create.send(sender='tool_add',toolname=tool.NAME)

        response_data['resultCode'] = '0000'
        response_data['resultDesc'] ="成功"
    except Exception, ex:
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = ex.__str__()
    log.info("leadinginTool end")
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")