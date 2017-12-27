# -*- coding: utf-8 -*
from django.forms.models import model_to_dict
from app_tower.models import T_JOB,T_JOB_EVENT,T_JOB_TEMPLATE,T_Group,T_LOGIN_CREDENTIALS,sudo_record,playbook,operation_record,T_PROJECT
from django.http import HttpRequest,HttpResponse,JsonResponse
from json import dumps
import os,re
from django.core import serializers
from django.shortcuts import render
import json
from app_tower.models import User
import tempfile
import traceback
from django.db import  transaction
from app_tower.tasks import run_playbook,runCommands,runCommands2
from celery.task.control import revoke
from celery.result import AsyncResult
from app_tower.utils import dateutil
from authority.permission import PermissionVerify
import logging
log = logging.getLogger("jobTempletedb")
#前往创建模板页面
def to_job_add(request):

    log.info("to_job_add start")
    groups=T_Group.objects.check_own(request)
    groupList = serializers.serialize('json', groups, ensure_ascii=False)
    credentials=T_LOGIN_CREDENTIALS.objects.check_own(request)
    credentialsList=serializers.serialize('json', credentials, ensure_ascii=False)
    playbooks=playbook.objects.check_own(request)
    playbooksList=serializers.serialize('json', playbooks, ensure_ascii=False)
    true = True
    null = None
    false=False
    log.info("groupList:"+groupList)
    log.info("credentialsList:"+credentialsList)
    log.info("playbooksList:"+playbooksList)
    log.info("to_job_add end")
    return render(request, 'templates/pages/app_tower_pages/jobTemplete/jobTemplate_create.html', {'groupList': eval(groupList), 'credentialsList':eval(credentialsList), 'playbooksList':eval(playbooksList)})

#description:添加任务模板
#params: request.POST {"NAME":"test","DESCRIPTION":"test","JOB_TYPE":"","GROUP_ID":"","PLAYBOOK_FILE":"","job_owner":"onlyOne","credentials":"credentialsId","FORKS":"1","JOB_TAGS":"","SKIP_TAGS":"","EXTRA_VARIABLES":"","LABELS":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def job_add(request):

    log.info("job_add start")
    log.info("request: "+str(request))
    form = {}
    response_data={}
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    try:
        if request.POST:
            form['NAME'] = request.POST['NAME']
            form['DESCRIPTION'] = request.POST['DESCRIPTION']
            form['JOB_TYPE'] = request.POST['JOB_TYPE']
            form['GROUP_ID'] = request.POST['GROUP_ID']
            form['PLAYBOOK_FILE'] = request.POST['PLAYBOOK_FILE']
            form['job_owner'] = request.POST['job_owner']
            form['credentials'] = request.POST['credentials']
            form['FORKS'] = request.POST['FORKS']
            form['JOB_TAGS'] = request.POST['JOB_TAGS']
            form['SKIP_TAGS'] = request.POST['SKIP_TAGS']
            form['EXTRA_VARIABLES'] = request.POST['EXTRA_VARIABLES']
            form['LABELS'] = request.POST['LABELS']
        log.info("form :"+str(form))

        if not T_Group.objects.check_id(request,form['GROUP_ID']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机组没有使用权限！"}))
        if not T_LOGIN_CREDENTIALS.objects.check_id(request,form['credentials']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"登录凭证没有使用权限！"}))
        if not playbook.objects.check_id(request,form['PLAYBOOK_FILE']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"playbook没有使用权限！"}))

        if form['job_owner']=='onlyOne':
            OWNER_ID=request.session['userId']
            OWNER_NAME=request.session['username']
        elif form['job_owner']=='all':
            OWNER_ALL=True
        else:
            if not T_PROJECT.objects.check_id(request,form['job_owner']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"项目组没有使用权限！"}))
            OWNER_PROJECT_ID=form['job_owner']
        userName=request.session['username']
        userId=request.session['userId']
        if T_JOB_TEMPLATE.objects.filter(NAME=form['NAME']):
            response_data['resultCode']='0001'
            response_data['resultDesc']='NAME已经存在，名称不能重复！'
            return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")
        job = T_JOB_TEMPLATE(NAME=form['NAME'],DESCRIPTION=form['DESCRIPTION'],JOB_TYPE=form['JOB_TYPE'],GROUP_ID=T_Group.objects.get(id=form['GROUP_ID']),EXTRA_VARIABLES=form['EXTRA_VARIABLES'],LABELS=form['LABELS'],
                             PLAYBOOK_ID=playbook.objects.get(id=form['PLAYBOOK_FILE']),PLAYBOOK_FILE=playbook.objects.get(id=form['PLAYBOOK_FILE']).PLAYBOOK_PATH,CREDENTIAL_MACHINE_ID=T_LOGIN_CREDENTIALS.objects.get(id=form['credentials']),  FORKS=form['FORKS'],JOB_TAGS=form['JOB_TAGS'],SKIP_TAGS=form['SKIP_TAGS'],
                             CREATE_USER_ID=userId,CREATE_USER_NAME=userName,OWNER_ID=OWNER_ID,OWNER_NAME=OWNER_NAME,OWNER_PROJECT_ID=OWNER_PROJECT_ID,OWNER_ALL=OWNER_ALL)
        job.save()
        log.info("job:"+str(model_to_dict(job)))
        response_data['resultCode']='0000'
        response_data['resultDesc']='添加成功！'
    except Exception, ex:
        print Exception, ex
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode']='0001'
        response_data['resultDesc']=ex.__str__()
    log.info("job_add end")
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#description:查询任务模板
#params: request.GET {"limit":5,"offset":0,"order":"asc","ordername":"id","name":"","description":""}
#return: {"resultCode":"","resultDesc":"","rows":"","total":""}
@PermissionVerify()
def job_select(request):

    log.info("job_select start")
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
        templeteList = T_JOB_TEMPLATE.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description).order_by(orderBy)
        total=len(templeteList)
        list = templeteList[int(offset):int(offset)+int(limit)]
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
    log.info("job_select end")
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#description:删除任务模板
#params: request.POST {"id":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def job_delete(request):

    log.info("job_delete start")
    log.info("request: "+str(request))
    form = {}

    if request.POST:
        form['id'] = request.POST['id']
        log.info("id:"+str(form))
    if not T_JOB_TEMPLATE.objects.check_id(request,form['id']):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"任务模板没有使用权限！"}))
    # 删除id的数据
    job = T_JOB_TEMPLATE.objects.get(id=form['id'])
    response_data = {}
    try:
        job.delete()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '删除成功！'
    except Exception,ex:
        print Exception,ex
        traceback.print_exc()
        log.error(ex)
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = '已被使用，禁止删除！'
    log.info("job_delete end")
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:修改任务模板
#params: request.POST {"id":"","NAME":"test","DESCRIPTION":"test","JOB_TYPE":"","GROUP_ID":"","PLAYBOOK_FILE":"","owner":"onlyOne","Login_credentials":"credentialsId","FORKS":"1","JOB_TAGS":"","SKIP_TAGS":"","EXTRA_VARIABLES":"","Labels":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def job_update(request):
    log.info("job_update start")
    log.info("request: "+str(request))
    form = {}
    response_data = {}
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    if not T_JOB_TEMPLATE.objects.check_id(request,request.POST['id']):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"任务模板没有使用权限！"}))
    if T_JOB_TEMPLATE.objects.filter(NAME=request.POST['NAME']).exists():
        if not T_JOB_TEMPLATE.objects.get(NAME=request.POST['NAME']).id == int(request.POST['id']):
            response_data['resultCode']='0001'
            response_data['resultDesc']='NAME已经存在，名称不能重复！'
            return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")
    try:
        if request.POST:
            form['id'] = request.POST['id']
            form['NAME'] = request.POST['NAME']
            form['DESCRIPTION'] = request.POST['DESCRIPTION']
            form['JOB_TYPE'] = request.POST['JOB_TYPE']
            form['GROUP_ID'] = request.POST['GROUP_ID']
            form['PLAYBOOK_FILE'] = request.POST['PLAYBOOK_FILE']
            form['FORKS'] = request.POST['FORKS']
            form['JOB_TAGS'] = request.POST['JOB_TAGS']
            form['SKIP_TAGS'] = request.POST['SKIP_TAGS']
            form['EXTRA_VARIABLES'] = request.POST['EXTRA_VARIABLES']
            form['Login_credentials'] = request.POST['Login_credentials']
            form['Labels'] = request.POST['Labels']
            form['owner'] = request.POST['owner']
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

            job = T_JOB_TEMPLATE.objects.get(id=form['id'])
            job.NAME = form['NAME']
            job.DESCRIPTION = form['DESCRIPTION']
            job.JOB_TYPE = form['JOB_TYPE']
            job.GROUP_ID = T_Group.objects.get(id=form['GROUP_ID'])
            if not form['PLAYBOOK_FILE']=='':

                job.PLAYBOOK_ID = playbook.objects.get(id=form['PLAYBOOK_FILE'])
                job.PLAYBOOK_FILE =playbook.objects.get(id=form['PLAYBOOK_FILE']).PLAYBOOK_PATH
            job.FORKS = form['FORKS']
            job.JOB_TAGS = form['JOB_TAGS']
            job.SKIP_TAGS = form['SKIP_TAGS']
            job.EXTRA_VARIABLES=form['EXTRA_VARIABLES']
            job.CREDENTIAL_MACHINE_ID=T_LOGIN_CREDENTIALS.objects.get(id=form['Login_credentials'])
            job.LABELS=form['Labels']
            job.MODIFY_USER_ID=request.session['userId']
            job.OWNER_ID=OWNER_ID
            job.OWNER_NAME=OWNER_NAME
            job.OWNER_PROJECT_ID=OWNER_PROJECT_ID
            job.OWNER_ALL=OWNER_ALL
            job.save()


            response_data['resultCode'] = '0000'
            response_data['resultDesc'] = '修改成功！'
    except Exception,ex:
        print Exception,ex
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = ex.__str__()
    log.info("job_update end")
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#description:保存并执行任务模板
#params: request.POST {"NAME":"test","DESCRIPTION":"test","JOB_TYPE":"","GROUP_ID":"","PLAYBOOK_FILE":"","job_owner":"onlyOne","credentials":"credentialsId","FORKS":"1","JOB_TAGS":"","SKIP_TAGS":"","EXTRA_VARIABLES":"","LABELS":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def save_run_job(request):

    log.info('save_run_job start')
    log.info("request: "+str(request))
    form = {}
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    response_data = {}
    try:
        form['NAME'] = request.POST['NAME']
        form['DESCRIPTION'] = request.POST['DESCRIPTION']
        form['JOB_TYPE'] = request.POST['JOB_TYPE']
        form['GROUP_ID'] = request.POST['GROUP_ID']
        form['PLAYBOOK_FILE'] = request.POST['PLAYBOOK_FILE']
        form['job_owner'] = request.POST['job_owner']
        form['credentials'] = request.POST['credentials']
        form['FORKS'] = request.POST['FORKS']
        form['JOB_TAGS'] = request.POST['JOB_TAGS']
        form['SKIP_TAGS'] = request.POST['SKIP_TAGS']
        form['EXTRA_VARIABLES'] = request.POST['EXTRA_VARIABLES']
        log.info("form:"+str(form))
        if not T_Group.objects.check_id(request,form['GROUP_ID']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机组没有使用权限！"}))
        if not T_LOGIN_CREDENTIALS.objects.check_id(request,form['credentials']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"登录凭证没有使用权限！"}))
        if not playbook.objects.check_id(request,form['PLAYBOOK_FILE']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"playbook没有使用权限！"}))

        if form['job_owner']=='onlyOne':
            OWNER_ID=request.session['userId']
            OWNER_NAME=request.session['username']
        elif form['job_owner']=='all':
            OWNER_ALL=True
        else:
            if not T_PROJECT.objects.check_id(request,form['job_owner']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"项目组没有使用权限！"}))
            OWNER_PROJECT_ID=form['job_owner']
        userName=request.session['username']
        userId=request.session['userId']
        if T_JOB_TEMPLATE.objects.filter(NAME=form['NAME']):
            response_data['resultCode']='0001'
            response_data['resultDesc']='NAME已经存在，名称不能重复！'
            return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

        #开启事物管理
        with transaction.atomic():
            job = T_JOB_TEMPLATE(NAME=form['NAME'], DESCRIPTION=form['DESCRIPTION'], JOB_TYPE=form['JOB_TYPE'],
                                 GROUP_ID=T_Group.objects.get(id=form['GROUP_ID']),CREDENTIAL_MACHINE_ID=T_LOGIN_CREDENTIALS.objects.get(id=form['credentials']),
                                 PLAYBOOK_FILE=playbook.objects.get(id=form['PLAYBOOK_FILE']).PLAYBOOK_PATH,PLAYBOOK_ID=playbook.objects.get(id=form['PLAYBOOK_FILE']), FORKS=form['FORKS'], JOB_TAGS=form['JOB_TAGS'],
                                 SKIP_TAGS=form['SKIP_TAGS'],EXTRA_VARIABLES=form['EXTRA_VARIABLES'],CREATE_USER_ID=userId,CREATE_USER_NAME=userName
                                 ,OWNER_ID=OWNER_ID,OWNER_NAME=OWNER_NAME,OWNER_PROJECT_ID=OWNER_PROJECT_ID,OWNER_ALL=OWNER_ALL)
            print job
            job.save()
            log.info(job.PLAYBOOK_FILE)
            file=tempfile.NamedTemporaryFile(delete=False)  #临时文件记录日志
            jobs = T_JOB(TEMPLETE_ID=job,NAME=job.NAME, DESCRIPTION=job.DESCRIPTION, JOB_TYPE=job.JOB_TYPE, GROUP_ID=job.GROUP_ID,
                         PROJECT_ID=job.PROJECT_ID, PLAYBOOK_ID=job.PLAYBOOK_ID,
                         PLAYBOOK_FILE=job.PLAYBOOK_FILE, CREDENTIAL_MACHINE_ID=job.CREDENTIAL_MACHINE_ID, FORKS=job.FORKS,
                         VERBOSITY=job.VERBOSITY, JOB_TAGS=job.JOB_TAGS,
                         SKIP_TAGS=job.SKIP_TAGS, EXTRA_VARIABLES=job.EXTRA_VARIABLES,
                         STATUS='STARTED',LOGFILE=file.name,CREATE_USER_ID=userId,CREATE_USER_NAME=userName
                         ,OWNER_ID=job.OWNER_ID,OWNER_NAME=job.OWNER_NAME,OWNER_PROJECT_ID=job.OWNER_PROJECT_ID,OWNER_ALL=job.OWNER_ALL)
            jobs.save()

        runbook = run_playbook.delay(file.name,jobs.id)
        taskid = runbook.task_id
        print taskid
        result = AsyncResult(taskid)
        T_JOB.objects.filter(id=jobs.id).update(STATUS=result.status,CELERY_TASK_ID=taskid)
        #result={'success': {'host':''}, 'fail': {'host':''}, 'unreachable': {'host':''}}

        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '成功'
        response_data['data'] = {'taskid':taskid,'name':job.NAME,'logfile':file.name,'userName':userName,'userId':userId,'runType':job.JOB_TYPE,'credentialId':job.CREDENTIAL_MACHINE_ID.id}
        response_data['jobsid'] = jobs.id
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    log.info('response_data:'+str(response_data))
    log.info('save_run_job end')
    return HttpResponse(JsonResponse(response_data), content_type='application/json')

#运行模板
@PermissionVerify()
def run_job(request):

    log.info('run_job start')
    log.info("request: "+str(request))
    form = {}
    response_data = {}
    try:
        form['id'] = request.POST['id']
        log.info("id:"+str(form))
        if not T_JOB_TEMPLATE.objects.check_id(request,form['id']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"任务模板没有使用权限！"}))
        form['jobTags']=""
        form['skipTags']=""
        form['variable']=""
        form['hostList']=None
        if request.POST['hostList']:
            form['hostList']=eval(request.POST['hostList'])
        if request.POST['jobTags']:
            form['jobTags']=request.POST['jobTags']
        if request.POST['skipTags']:
            form['skipTags']=request.POST['skipTags']
        if request.POST['variable']:
            form['variable']=request.POST['variable']
        userName=request.session['username']
        userId=request.session['userId']

        #开启事物管理
        with transaction.atomic():
            job = T_JOB_TEMPLATE.objects.get(id=form['id'])
            job.JOB_TAGS=form['jobTags']
            job.SKIP_TAGS=form['skipTags']
            job.EXTRA_VARIABLES=form['variable']
            job.save()
            file=tempfile.NamedTemporaryFile(delete=False)  #临时文件记录日志
            jobs=T_JOB(TEMPLETE_ID=job,NAME=job.NAME,DESCRIPTION=job.DESCRIPTION,JOB_TYPE=job.JOB_TYPE,GROUP_ID=job.GROUP_ID,PROJECT_ID=job.PROJECT_ID,PLAYBOOK_ID=job.PLAYBOOK_ID,
                       PLAYBOOK_FILE=job.PLAYBOOK_FILE,CREDENTIAL_MACHINE_ID=job.CREDENTIAL_MACHINE_ID,FORKS=job.FORKS,VERBOSITY=job.VERBOSITY,JOB_TAGS=job.JOB_TAGS,
                       SKIP_TAGS=job.SKIP_TAGS,EXTRA_VARIABLES=job.EXTRA_VARIABLES,STATUS='STARTED',LOGFILE=file.name,CREATE_USER_ID=userId,CREATE_USER_NAME=userName
                       ,OWNER_ID=job.OWNER_ID,OWNER_NAME=job.OWNER_NAME,OWNER_PROJECT_ID=job.OWNER_PROJECT_ID,OWNER_ALL=job.OWNER_ALL)
            jobs.save()

        log.info("jobs:"+str(model_to_dict(jobs)))
        runbook = run_playbook.delay(file.name,jobs.id,form['hostList'])
        taskid = runbook.task_id
        print taskid
        # runbook=runplaybook(job.id,'/usr/local/vega/logs/runlog.txt')
        # result=runbook.run()
        result = AsyncResult(taskid)
        log.info("STATUS:"+result.status)
        T_JOB.objects.filter(id=jobs.id).update(STATUS=result.status,CELERY_TASK_ID=taskid)


        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '成功'
        response_data['data'] = {'taskid':taskid,'name':job.NAME,'logfile':file.name,'userName':userName,'userId':userId,'runType':job.JOB_TYPE,'credentialId':job.CREDENTIAL_MACHINE_ID.id}
        response_data['jobsid'] = jobs.id
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    log.info('response_data:'+str(response_data))
    log.info('run_job end')
    return HttpResponse(JsonResponse(response_data), content_type='application/json')

#前往任务执行页面
def to_job_run(request):

    print 'url to_job_run'
    jobsid=request.GET.get('jobsid')
    if not T_JOB.objects.check_id(request,jobsid):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"任务没有使用权限！"}))
    jobs=T_JOB.objects.get(id=jobsid)
    print jobsid
    return render(request, 'templates/pages/app_tower_pages/jobTemplete/jobTemplate_run.html', {'jobsid': jobs})


#实时读取运行日志

def read_job_log(request):

    log.info('read_job_log start')
    log.info("request: "+str(request))
    try:
        seek=0
        if request.POST['seek']:
            seek=request.POST['seek']
        taskid=request.POST['taskid']
        logfile=request.POST['logfile']

        jobsid=request.POST['jobsid']

        response_data = {}
        jobs=T_JOB.objects.get(id=jobsid)
        state=jobs.STATUS
        response_data['state']=state
        log.info('state:'+state)
        if not os.access(logfile, os.F_OK):
           #临时文件不存在
            response_data['log']=jobs.LOGCONTENT
            response_data['seek']=0
        else :
            with open(logfile,'r') as f:
                f.seek(0)
                response_data['log'] =f.read()
                response_data['seek']=f.tell()


        response_data['jobs']={'startTime':json.dumps(jobs.START_TIME, cls=dateutil.CJsonEncoder),
                               'endTime':json.dumps(jobs.FINISH_TIME, cls=dateutil.CJsonEncoder),'elapsed':jobs.ELAPSED,'runType':jobs.JOB_TYPE,'playbookPath':jobs.PLAYBOOK_FILE}
        group=T_Group.objects.get(id=jobs.GROUP_ID.id)
        response_data['groupName']=group.NAME
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

#停止任务
@PermissionVerify()
def stop_job(request):
    log.info('stop_job start')
    log.info("request: "+str(request))
    taskid=request.POST['taskid']
    jobsid=request.POST['jobsid']
    if not T_JOB.objects.check_id(request,jobsid):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"任务没有使用权限！"}))
    revoke(taskid,terminate=True,signal='SIGKILL')
    result=AsyncResult(taskid)
    T_JOB.objects.filter(id=jobsid).update(STATUS='REVOKED',CANCEL_FLAG=True)
    log.info('stop_job end status'+result.status)
    return HttpResponse(json.dumps({'success':'true','status':result.status}))




#检查分发文件
def checkFile(request):

    taskid=request.POST['taskid']
    logfile=request.POST['logfile']
    desPath=request.POST['desPath']
    groupid=int(request.POST['groupid'])
    hostList=eval(request.POST['hostList'])
    credentialsid=request.POST['credentialsid']
    if groupid!=0:
        if not T_Group.objects.check_id(request,groupid):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机组没有使用权限！"}))
    if not T_LOGIN_CREDENTIALS.objects.check_id(request,credentialsid):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"登录凭证没有使用权限！"}))
    vars="ls -al "+desPath
    result = runCommands2.delay(logfile,groupid,credentialsid,"shell",vars,request.session['userId'],request.session['username'],hostList)
    taskid = result.task_id
    return HttpResponse(json.dumps({'start':'true','file':logfile,'taskid':taskid}))

def run_commands2(request):

    groupid=int(request.POST['groupid'])
    hostList=eval(request.POST['hostList'])
    credentialsid=request.POST['credentialsid']
    if groupid!=0:
        if not T_Group.objects.check_id(request,groupid):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机组没有使用权限！"}))
    if not T_LOGIN_CREDENTIALS.objects.check_id(request,credentialsid):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"登录凭证没有使用权限！"}))
    commandName=request.POST['commandName']
    vars=request.POST['vars']
    file=tempfile.NamedTemporaryFile(delete=False)  #临时文件记录日志

    result = runCommands2.delay(file.name,groupid,credentialsid,commandName,vars,request.session['userId'],request.session['username'],hostList)
    taskid = result.task_id
    return HttpResponse(json.dumps({'start':'true','file':file.name,'taskid':taskid}))
#查找SN号
@PermissionVerify()
def run_commands_searchSN(request):

    groupid=int(request.POST['groupid'])
    hostList=eval(request.POST['hostList'])
    credentialsid=request.POST['credentialsid']
    if groupid!=0:
        if not T_Group.objects.check_id(request,groupid):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机组没有使用权限！"}))
    if not T_LOGIN_CREDENTIALS.objects.check_id(request,credentialsid):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"登录凭证没有使用权限！"}))
    commandName="shell"
    vars="dmidecode -t 1 | grep Serial"
    file=tempfile.NamedTemporaryFile(delete=False)  #临时文件记录日志

    result = runCommands2.delay(file.name,groupid,credentialsid,commandName,vars,request.session['userId'],request.session['username'],hostList)
    taskid = result.task_id
    return HttpResponse(json.dumps({'start':'true','file':file.name,'taskid':taskid}))

#日志查询
@PermissionVerify()
def run_commands_searchLog(request):

    groupid=int(request.POST['groupid'])
    hostList=eval(request.POST['hostList'])
    credentialsid=request.POST['credentialsid']
    if groupid!=0:
        if not T_Group.objects.check_id(request,groupid):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机组没有使用权限！"}))
    if not T_LOGIN_CREDENTIALS.objects.check_id(request,credentialsid):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"登录凭证没有使用权限！"}))
    cmd=request.POST['cmd']
    content=request.POST['content']
    path=request.POST['path']
    commandName="shell"
    vars = cmd+" "+content+" "+path
    file=tempfile.NamedTemporaryFile(delete=False)  #临时文件记录日志

    result = runCommands2.delay(file.name,groupid,credentialsid,commandName,vars,request.session['userId'],request.session['username'],hostList)
    taskid = result.task_id
    return HttpResponse(json.dumps({'start':'true','file':file.name,'taskid':taskid}))

#分发文件
@PermissionVerify()
def run_commands_copyFile(request):

    groupid=int(request.POST['groupid'])
    hostList=eval(request.POST['hostList'])
    credentialsid=request.POST['credentialsid']
    if groupid!=0:
        if not T_Group.objects.check_id(request,groupid):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机组没有使用权限！"}))
    if not T_LOGIN_CREDENTIALS.objects.check_id(request,credentialsid):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"登录凭证没有使用权限！"}))
    srcPath=request.POST['srcPath']
    desPath=request.POST['desPath']
    commandName="copy"
    vars = "src="+srcPath+" "+"dest="+desPath;
    file=tempfile.NamedTemporaryFile(delete=False)  #临时文件记录日志

    result = runCommands2.delay(file.name,groupid,credentialsid,commandName,vars,request.session['userId'],request.session['username'],hostList)
    taskid = result.task_id
    return HttpResponse(json.dumps({'start':'true','file':file.name,'taskid':taskid}))
#修改sudo权限
@PermissionVerify()
def run_commands_changeSudoAuth(request):
    log.info('run_commands_changeSudoAuth start')
    log.info(str(request.body))

    response_data={}

    hostList=eval(request.POST['hostList'])

    credentialsid=request.POST['credentialsid']

    if not T_LOGIN_CREDENTIALS.objects.check_id(request,credentialsid):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"登录凭证没有使用权限！"}))
    userName=request.POST['userName']
    if userName=='' :
        userName='version'
    if userName=='root' or userName=='manage':
        response_data['resultCode']='0001'
        response_data['resultDesc']='不能修改root用户和manage用户！'
        return HttpResponse(JsonResponse(response_data), content_type='application/json')
    action=request.POST['action']
    port =request.POST['port']
    requestDesc=request.POST['requestUser']
    vars=""
    commandName=""
    groupid=None
    if action=='add':
        vars="dest=/etc/sudoers insertafter='^sre' line='"+userName+" ALL=(ALL) NOPASSWD:ALL' validate='visudo -cf %s'"
        commandName='lineinfile'
    elif action=='cancel':
        vars="dest=/etc/sudoers state=absent regexp='^("+userName+" .*)$' validate='visudo -cf %s'"
        commandName='lineinfile'
    elif action=='search':
        vars= "grep -e '"+userName+"' /etc/sudoers"
        commandName='shell'
    elif action=='searchFile':
        vars= "cat /etc/sudoers"
        commandName='shell'
    file=tempfile.NamedTemporaryFile(delete=False)  #临时文件记录日志


    result = runCommands2.delay(file.name,groupid,credentialsid,commandName,vars,request.session['userId'],request.session['username'],hostList,port,'true',action,userName,requestDesc)
    taskid = result.task_id
    log.info('run_commands_changeSudoAuth end')
    return HttpResponse(json.dumps({'resultCode':'0000','resultDesc':'开始执行','start':'true','file':file.name,'taskid':taskid}))

#回收sudo权限
@PermissionVerify()
def run_commands_callbackSudoAuth(request):
    log.info('run_commands_callbackSudoAuth start')
    log.info(str(request.body))

    response_data={}
    sudoIdList=eval(request.POST['sudoIdList'])
    for sudoId in sudoIdList:
        sudoRecord=sudo_record.objects.get(id=int(sudoId))
        hostName=sudoRecord.IP
        hostList=[]
        hostList.append(hostName)
        credentialsid=sudoRecord.CREDENTIALS_ID.id
        userName=sudoRecord.ACCOUNT

        action='cancel'
        port =sudoRecord.PORT
        requestDesc=u"回收权限"
        vars=""
        commandName=""
        groupid=None

        vars="dest=/etc/sudoers state=absent regexp='^("+userName+" .*)$' validate='visudo -cf %s'"
        commandName='lineinfile'

        file=tempfile.NamedTemporaryFile(delete=False)  #临时文件记录日志


        result = runCommands2.delay(file.name,groupid,credentialsid,commandName,vars,request.session['userId'],request.session['username'],hostList,port,'true',action,userName,requestDesc)
        taskid = result.task_id
    log.info('run_commands_callbackSudoAuth end')
    return HttpResponse(json.dumps({'resultCode':'0000','resultDesc':'开始执行','start':'true',}))

#查询进程
@PermissionVerify()
def run_commands_searchProcess(request):
    log.info('run_commands_searchProcess start')
    log.info(str(request.body))

    hostList=eval(request.POST['hostList'])
    credentialsid=request.POST['credentialsid']
    if not T_LOGIN_CREDENTIALS.objects.check_id(request,credentialsid):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"登录凭证没有使用权限！"}))
    processName=request.POST['processName']
    commandName="shell"
    vars = "ps -elf | grep "+processName+" | grep -v 'grep'"
    file=tempfile.NamedTemporaryFile(delete=False)  #临时文件记录日志

    result = runCommands2.delay(file.name,None,credentialsid,commandName,vars,request.session['userId'],request.session['username'],hostList)
    taskid = result.task_id
    log.info(taskid)
    log.info('run_commands_searchProcess end')
    return HttpResponse(json.dumps({'start':'true','file':file.name,'taskid':taskid}))


#修改进程
@PermissionVerify()
def run_commands_changeProcess(request):
    log.info('run_commands_changeProcess start')
    log.info(str(request.body))

    hostList=eval(request.POST['hostList'])
    credentialsid=request.POST['credentialsid']
    if not T_LOGIN_CREDENTIALS.objects.check_id(request,credentialsid):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"登录凭证没有使用权限！"}))
    processName=request.POST['processName']
    operation=request.POST['operation']
    commandName="service"
    vars = ''
    if operation=='started':
        vars="name="+processName+" state="+operation
    if operation=='restarted':
        vars="name="+processName+" state="+operation
    # if operation=='reloaded':
    #     vars="name="+processName+" state="+operation
    if operation=='stopped':
        vars="name="+processName+" state="+operation
    # if operation=='yes':
    #     vars="name="+processName+" enabled="+operation
    # if operation=='no':
    #     vars="name="+processName+" enabled="+operation
    file=tempfile.NamedTemporaryFile(delete=False)  #临时文件记录日志

    result = runCommands2.delay(file.name,None,credentialsid,commandName,vars,request.session['userId'],request.session['username'],hostList)
    taskid = result.task_id
    log.info(taskid)
    log.info('run_commands_changeProcess end')
    return HttpResponse(json.dumps({'start':'true','file':file.name,'taskid':taskid}))

#执行SH脚本
@PermissionVerify()
def run_commands_runSH(request):
    log.info('run_commands_runSH start')
    log.info(str(request.body))

    groupid=int(request.POST['groupid'])
    hostList=eval(request.POST['hostList'])
    credentialsid=request.POST['credentialsid']
    if groupid!=0:
        if not T_Group.objects.check_id(request,groupid):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机组没有使用权限！"}))
    if not T_LOGIN_CREDENTIALS.objects.check_id(request,credentialsid):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"登录凭证没有使用权限！"}))
    commandName="script"
    vars=request.POST['vars']
    fo=open("/tmp/runSH.sh","wb")
    fo.write(vars)
    fo.close()
    file=tempfile.NamedTemporaryFile(delete=False)  #临时文件记录日志

    result = runCommands2.delay(file.name,groupid,credentialsid,commandName,"/tmp/runSH.sh",request.session['userId'],request.session['username'],hostList)
    taskid = result.task_id
    return HttpResponse(json.dumps({'start':'true','file':file.name,'taskid':taskid}))

def read_commands_log(request):

    log.info('read_job_log start')
    seek=0

    taskid=request.POST['taskid']
    logfile=request.POST['logfile']
    response_data = {}
    result = AsyncResult(taskid)
    state=result.status
    response_data['state']=state
    log.info('state:'+state)

    with open(logfile,'r+') as f:
        f.seek(0)
        response_data['log'] =f.read()
        response_data['seek']=f.tell()

    if response_data['state'] in ['SUCCESS','FAILURE','REVOKED']:
        response_data['read_flag']='False'
    else:
        response_data['read_flag']='True'
    log.info('read_commands_log end')
    return HttpResponse(json.dumps(response_data))
    #ansible_playbook = '/root/code/ping.yml'
    #bits = 'set -o pipefail;ansible-playbook {0}|tee -a /tmp/ansible.log'.format(ansible_playbook)
    #(status, output) = commands.getstatusoutput('bash -c {0}'.format(bits))
    #(status, output) = commands.getstatusoutput("set -o pipefail;"+commands+"|tee -a "+file)

    # if status != 0:
    #     return HttpResponse({'msg': '{0} has not been touched'.format('ggg'), 'output': output})
    # return HttpResponse({'msg': '{0} has beentouched'.format('ggg'), 'output': output})

def init_commands_select(request):
    log.info("init_commands_select start")
    groups=T_Group.objects.check_own(request)
    groupList = serializers.serialize('json', groups, ensure_ascii=False)
    credentials=T_LOGIN_CREDENTIALS.objects.check_own(request)
    credentialsList=serializers.serialize('json', credentials, ensure_ascii=False)
    playbooks=playbook.objects.check_own(request)
    playbooksList=serializers.serialize('json', playbooks, ensure_ascii=False)
    true = True
    null = None
    false=False
    log.info("groupList:"+groupList)
    log.info("credentialsList:"+credentialsList)
    log.info("playbooksList:"+playbooksList)
    log.info("init_commands_select end")
    return HttpResponse(json.dumps({'groupList': eval(groupList),'credentialsList':eval(credentialsList),'playbooksList':eval(playbooksList)}))

def get_event(request):
    jobsid=request.POST['jobsid']
    job_event=T_JOB_EVENT.objects.filter(JOB_ID=jobsid)
    eventList= serializers.serialize('json', job_event,ensure_ascii=False)
    return HttpResponse(json.dumps({'eventList':eval(eventList)}))

#预览文件（playbook）
def review_file(request):
    log.info('review_file start')
    request.session['username'] = request.session['username']
    request.session['userId'] = User.objects.get(username=request.session['username']).id

    response_data = {}
    playbookId=request.POST['filePath']
    playbookPath=playbook.objects.get(id=int(playbookId)).PLAYBOOK_PATH
    if not os.access(playbookPath, os.F_OK):
        response_data['resultCode']='0001'
        response_data['resultDesc']='文件不存在'
        return HttpResponse(json.dumps(response_data))
    else:
        with open(playbookPath,'r+') as f:
            f.seek(0)
            response_data['fileContent'] =f.read()

        response_data['resultCode']='0000'
        response_data['resultDesc']='Success'
        log.info('review_file end')
        return HttpResponse(json.dumps(response_data))

@PermissionVerify()
def sudo_select(request):

    log.info("sudo_select start")
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
    ip = ''
    account = ''
    createUser=''
    if request.GET.get("ip"):
        ip=request.GET.get("ip")
    if request.GET.get("account"):
        account=request.GET.get("account")
    if request.GET.get("createUser"):
        createUser=request.GET.get("createUser")

    # 排序字段
    # ordername= request.GET.get('ordername')
    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM     Test.objects.filter(name="runoob").order_by("id")
    templeteList = sudo_record.objects.filter(IP__contains=ip).filter(ACCOUNT__contains=account).filter(CREATE_USER_NAME__contains=createUser).order_by(orderBy)
    total=len(templeteList)

    try:
        list = templeteList[int(offset):int(offset)+int(limit)]
        #[5:10]这是查找从下标5到下标10之间的数据，不包括10。
    except Exception,ex:
        print Exception,ex
        log.error(ex)
    response_data = {}
    try:
        response_data['result'] = 'Success'
        #序列码 serializers.serialize，且ensure_ascii=False防止乱码
        response_data['rows'] = serializers.serialize('json', list,ensure_ascii=False,use_natural_keys=True)
        response_data['total'] = total
    except:
        response_data['result'] = 'FAIELD!'
        response_data['rows'] = 'Script has not ran correctly'
    log.info('response_data:'+str(response_data))
    log.info("sudo_select end")
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

@PermissionVerify()
def sudoRecord_add(request):
    log.info("sudoRecord_add start")
    form={}
    try:
        form['ip']=request.POST['addIP']
        form['port']=request.POST['addPort']
        form['account']=request.POST['addAccount']
        form['des']=request.POST['addDesc']
        sudorecord=sudo_record(IP=form['ip'],ACCOUNT=form['account'],DESCRIPTION=form['des'],PORT=form['port'],CREATE_USER_ID=request.session['userId'],CREATE_USER_NAME=request.session['username'])
        sudorecord.save()
        return HttpResponse(JsonResponse({"resultCode":"0000","resultDesc":"添加成功！"}), content_type="application/json;charset=UTF-8")
    except Exception,e:
        log.error(e.__str__())
        return HttpResponse(JsonResponse({"resultCode":"0001","resultDesc":e.__str__()}), content_type="application/json;charset=UTF-8")
    finally:
        log.info("sudoRecord_add end")

@PermissionVerify()
def sudo_delete(request):
    log.info("sudoRecord_delete start")

    try:
        id=request.POST['id']
        sudorecord=sudo_record.objects.get(id=id)
        sudorecord.delete()

        return HttpResponse(JsonResponse({"resultCode":"0000","resultDesc":"删除成功！"}), content_type="application/json;charset=UTF-8")
    except Exception,e:
        log.error(e.__str__())
        return HttpResponse(JsonResponse({"resultCode":"0001","resultDesc":e.__str__()}), content_type="application/json;charset=UTF-8")
    finally:
        log.info("sudoRecord_delete end")

@PermissionVerify()
def operation_select(request):

    log.info("operation_select start")
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
    ip = ''
    name = ''
    createUser=''
    if request.GET.get("ip"):
        ip=request.GET.get("ip")
    if request.GET.get("name"):
        name=request.GET.get("name")
    if request.GET.get("createUser"):
        createUser=request.GET.get("createUser")

    # 排序字段
    # ordername= request.GET.get('ordername')
    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM     Test.objects.filter(name="runoob").order_by("id")
    templeteList = operation_record.objects.filter(CREATE_USER_NAME__contains=createUser).filter(NAME__contains=name)
    total=len(templeteList)

    try:
        list = templeteList[int(offset):int(offset)+int(limit)]
        #[5:10]这是查找从下标5到下标10之间的数据，不包括10。
    except Exception,ex:
        print Exception,ex
        log.error(ex)
    response_data = {}
    try:
        response_data['result'] = 'Success'
        #序列码 serializers.serialize，且ensure_ascii=False防止乱码
        response_data['rows'] = serializers.serialize('json', list,ensure_ascii=False,use_natural_keys=True)
        response_data['total'] = total
    except:
        response_data['result'] = 'FAIELD!'
        response_data['rows'] = 'Script has not ran correctly'
    log.info('response_data:'+str(response_data))
    log.info("sudo_select end")
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

def get_match(match_content):
    number_list=['1','2','3','4','5','6','7','8','9','0']
    q_list=['q','w','e','r','t','y','u','i','o','p']
    a_list=['a','s','d','f','g','h','j','k','l','\;','\'']
    z_list=['z','x','c','v','b','n','m','\,','\.','\/']
    all_number,all_q,all_a,all_z='1234567890','qwertyuiop','asdfghjkl;','zxcvbnm,./'
    for n in range(0,10):
        may_words=number_list[n]+q_list[n]+a_list[n]+z_list[n]
        if re.search(match_content,may_words):
            return may_words
        elif re.search(match_content,may_words[::-1]):
            return may_words[::-1]
    if match_content in all_number:
        return all_number
    elif match_content in all_number[::-1]:
        return all_number[::-1]
    elif match_content in all_q[::-1]:
        return all_q[::-1]
    elif match_content in all_q:
        return all_q
    elif match_content in all_a:
        return all_a[::-1]
    elif match_content in all_a[::-1]:
        return all_a[::-1]
    elif match_content in all_z:
        return all_z[::-1]
    elif match_content in all_z[::-1]:
        return all_z[::-1]
@PermissionVerify()
def run_commands_change_passwd(request):

    groupid=None
    hostList=eval(request.POST['hostList'])
    credentialsid=request.POST['changepwd_credentials']
    if not T_LOGIN_CREDENTIALS.objects.check_id(request,credentialsid):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"登录凭证没有使用权限！"}))
    new_pwd=request.POST['new_pwd']
    user_name=request.POST['user_name']
    commandName="user"
    regexes = [re.compile(check_pwd) for check_pwd in ['[A-Z]','[0-9]','[a-z]','[\.\,\/\;\'\[\]\{\}\\\|\:\"\<\>\?\~\!\@\#\$\%\^\&\*\(\)\-\_\=\+]']]
    if len(new_pwd)<8:
        return HttpResponse(json.dumps({'resultCode':'0060'}))
    for regex in regexes:
        if not regex.search(new_pwd):
            return HttpResponse(json.dumps({'resultCode':'0059'}))
    for k in range (3,len(new_pwd)):
        match_content=new_pwd[k-3]+new_pwd[k-2]+new_pwd[k-1]+new_pwd[k]
        will_info=get_match(match_content)
        if will_info:
            return HttpResponse(json.dumps({'resultCode':'0058'}))
    output = os.popen('openssl passwd -salt -1 "%s"' % new_pwd)
    pwd_line=[]
    for every_line in output.readlines():
        pwd_line.append(every_line)
    will_pwd=re.sub('\n','',pwd_line[0])
    vars="name=%s password=%s update_password=always" % (user_name,will_pwd)
    file=tempfile.NamedTemporaryFile(delete=False)  #临时文件记录日志
    result = runCommands2.delay(file.name,groupid,credentialsid,commandName,vars,request.session['userId'],request.session['username'],hostList)
    taskid = result.task_id
    return HttpResponse(json.dumps({'start':'true','file':file.name,'taskid':taskid}))