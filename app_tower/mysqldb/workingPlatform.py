#!/usr/bin/env python
# -*- coding:utf8 -*-
from app_tower.models import T_TOOL,T_TOOL_INPUT,T_TOOL_OUTPUT,T_TOOLTYPE,T_PROJECT,T_TOOL_User_ID,User,T_LOGIN_CREDENTIALS,T_TOOL_EVENT
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from json import dumps
import json
import tempfile
import traceback
import os
from app_tower.utils import dateutil
from django.db import  transaction
from django.core import serializers
from app_tower.tasks import run_tool_yaml
from celery.task.control import revoke
from celery.result import AsyncResult
from django.utils.timezone import now, timedelta
from authority.permission import PermissionVerify
import logging
log = logging.getLogger("project")

#初始化作业平台
def working_init(request):
    log.info('working_init start')
    toolType=T_TOOLTYPE.objects.all()
    toolTypeList = serializers.serialize('json', toolType, ensure_ascii=False)
    tool=User.objects.get(id=request.session['userId']).tools.all()
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

    tool=T_TOOL.objects.all()
    for t in tool:
        t.ARGS1=t.TOOLTYPE_ID.NAME
    toolList = serializers.serialize('json', tool, ensure_ascii=False)


    true = True
    false=False
    null = None
    #log.info('userList：'+userList)
    log.info('toolshop_init end')
    return HttpResponse(json.dumps({'resultCode':'0000','tools': eval(toolList)}))

#初始化工具创建页面
def toolcreate_init(request):
    log.info('toolcreate_init start')

    tooltype=T_TOOLTYPE.objects.all()
    tooltypeList = serializers.serialize('json', tooltype, ensure_ascii=False)
    project=T_PROJECT.objects.check_own(request)
    projectList = serializers.serialize('json', project, ensure_ascii=False)

    true = True
    false=False
    null = None
    #log.info('userList：'+userList)
    log.info('toolcreate_init end')
    return HttpResponse(json.dumps({'resultCode':'0000','tooltypeList': eval(tooltypeList),'projectList': eval(projectList)}))

#初始化工具明细
def toolDetail_init(request):
    log.info('toolDetail_init start')
    toolid=request.POST['toolid']
    tool=T_TOOL.objects.get(id=int(toolid))
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
    log.info('toolDetail_init start')
    toolid=request.POST['toolid']
    tool=T_TOOL.objects.get(id=int(toolid))
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
    true = True
    false=False
    null = None
    #log.info('userList：'+userList)
    log.info('toolDetail_init end')
    print str(model_to_dict(tool))
    return HttpResponse(json.dumps({'resultCode':'0000','tool':model_to_dict(tool),'toolinput': eval(toolinputList),'tooloutput': eval(tooloutputList),'tooltypeList': eval(tooltypeList),'projectList': eval(projectList)}))


#初始化历史任务
def toolEvent_init(request):
    log.info('toolEvent_init start')
    toolEventId=request.POST['toolEventId']
    toolEvent=T_TOOL_EVENT.objects.get(id=int(toolEventId))
    toolEvent.ARGS1=toolEvent.TOOL_ID.NAME
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

#description:添加工具
#params: request.POST {"name":"","type":"","language":"","scriptCode":"","des":"","inputParam":"[]","outputParam":"[]","owner":""}
#return: {"resultCode":"","resultDesc":""}

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
            tool = T_TOOL(NAME=form['name'], DESCRIPTION=form['des'], TOOLTYPE_ID=tooltype,SCRIPT_LANGUAGE=form['language'],SCRIPT_CODE=form['scriptCode'],
                             OWNER_ID=OWNER_ID, OWNER_NAME=OWNER_NAME, OWNER_PROJECT_ID=OWNER_PROJECT_ID, OWNER_ALL=OWNER_ALL,
                                CREATE_USER_ID=request.session['userId'],CREATE_USER_NAME=request.session['username'])
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
            form['name'] = request.POST['name']
            form['type'] = request.POST['type']
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

            T_TOOL.objects.filter(id=int(form['toolid'])).update(NAME=form['name'], DESCRIPTION=form['des'], TOOLTYPE_ID=tooltype,SCRIPT_LANGUAGE=form['language'],SCRIPT_CODE=form['scriptCode'],
                                                                      OWNER_ID=OWNER_ID, OWNER_NAME=OWNER_NAME, OWNER_PROJECT_ID=OWNER_PROJECT_ID, OWNER_ALL=OWNER_ALL,
                                                                      MODIFY_USER_ID=request.session['userId'])

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
        if request.GET.get("name"):
            name=request.GET.get("name")
        if request.GET.get("description"):
            description=request.GET.get("description")

        # 排序字段
        # ordername= request.GET.get('ordername')
        # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM     Test.objects.filter(name="runoob").order_by("id")
        toolList = T_TOOL.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description).order_by(orderBy)
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

def importTool(request):
    response_data={}
    try:
        toolId=request.POST['toolId']
        if not T_TOOL.objects.check_id(request,int(toolId)):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"工具没有使用权限！"}))
        user=User.objects.get(id=int(request.session['userId']))
        tool=T_TOOL.objects.get(id=int(toolId))
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


#description:移除工具
#params: request.POST {"toolId":""}
#return: {"resultCode":"","resultDesc":""}

def removeTool(request):
    response_data={}
    try:
        toolId=request.POST['toolId']

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

def tool_run(request):
    response_data={}
    form={}
    try:
        if request.POST:
            form['toolid']=request.POST['toolid']
            form['credentialsId']=request.POST['credentials']
            form['hostList']=request.POST['hostList']
            form['inputParams']=request.POST['inputParams']
        print str(form)
        tool=T_TOOL.objects.get(id=int(form['toolid']))
        file=tempfile.NamedTemporaryFile(delete=False)  #临时文件记录日志
        tool_event=T_TOOL_EVENT(TOOL_ID=tool,CREDENTIALS_ID_id=int(form['credentialsId']),HOSTLIST=form['hostList'],INPUTPARAMS=form['inputParams'],CREATE_USER_ID=request.session['userId'],
                     CREATE_USER_NAME=request.session['username'],LOGFILE=file.name,STATUS='STARTED',OWNER_ID=tool.OWNER_ID,OWNER_NAME=tool.OWNER_NAME,OWNER_PROJECT_ID=tool.OWNER_PROJECT_ID,OWNER_ALL=tool.OWNER_ALL)
        tool_event.save()

        if tool.SCRIPT_LANGUAGE==2:
            jobTags=[]
            skipTags=[]
            extraVariable={}
            for param in eval(form['inputParams']):
                if param['type']=='5':
                    jobTags.append(param['value'])
                elif param['type']=='6':
                    skipTags.append(param['value'])
                elif param['type']=='7':
                    extraVariable[param['name']]=param['value']
            #临时playbook
            playbook=tempfile.NamedTemporaryFile(delete=False)
            fo = open(playbook.name, "r+")
            fo.write(tool.SCRIPT_CODE)
            fo.flush()
            runtool = run_tool_yaml.delay(tool_event.id,int(form['credentialsId']),file.name,playbook.name,jobTags,skipTags,extraVariable,hostList=eval(request.POST['hostList']))
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


#实时读取运行日志

def read_log(request):

    log.info('read_job_log start')
    log.info("request: "+str(request))
    try:
        seek=0
        if request.POST['seek']:
            seek=request.POST['seek']
        taskid=request.POST['taskid']
        logfile=request.POST['logfile']

        toolEventId=request.POST['toolEventId']

        response_data = {}
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