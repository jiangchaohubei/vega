#!/usr/bin/env python
# -*- coding:utf8 -*-
from app_tower.models import T_JOB_TEMPLATE,T_PROJECT,TimerTask
from djcelery import models as celery_models
from django.http import HttpRequest,HttpResponse,JsonResponse
import json
from django.core import serializers
from django.utils import timezone
from django.db import  transaction

import traceback
from authority.permission import PermissionVerify
import logging
log = logging.getLogger("timerTask")


def init_jobTemplete_select(request):
    log.info("init_jobTemplete_select start" )
    jobTemplete=T_JOB_TEMPLATE.objects.check_own(request)
    jobTempleteList = serializers.serialize('json', jobTemplete, ensure_ascii=False)
    true = True
    null = None
    false=False
    log.info("init_jobTemplete_select end" )
    return HttpResponse(json.dumps({'jobTempleteList': eval(jobTempleteList)}))

@PermissionVerify()
def timerTask_add(request):
    log.info("timerTask_add start" )
    log.info("request: "+str(request))
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    try:

        form={}
        form["timerTask_name"]=request.POST["timerTask_name"]
        form["timerTask_desc"]=request.POST["timerTask_desc"]
        form["timerTask_jobTemplete"]=request.POST["timerTask_jobTemplete"]
        if not T_JOB_TEMPLATE.objects.check_id(request,form["timerTask_jobTemplete"]):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"任务模板没有使用权限！"}))
        form["timerTask_isUse"]=request.POST["timerTask_isUse"]
        form["timerTask_startTime"]=request.POST["timerTask_startTime"]
        form["timerTask_every"]=request.POST["timerTask_every"]
        if form["timerTask_startTime"]  and  form["timerTask_every"] :
                return HttpResponse(json.dumps({"resultCode":"0001","resultDesc":"开始时间和间隔时间二选一！"}))
        form["timerTask_period"]=request.POST["timerTask_period"]
        form["timerTask_expiresTime"]=request.POST["timerTask_expiresTime"]
        form["timerTask_owner"]=request.POST["timerTask_owner"]
        log.info("form:"+str(form))
        if form['timerTask_owner']=='onlyOne':
            OWNER_ID=request.session['userId']
            OWNER_NAME=request.session['username']
        elif form['timerTask_owner']=='all':
            OWNER_ALL=True
        else:
            if not T_PROJECT.objects.check_id(request,form['timerTask_owner']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"项目组没有使用权限！"}))
            OWNER_PROJECT_ID=form['timerTask_owner']
        userName=request.session['username']
        userId=request.session['userId']
        if TimerTask.objects.filter(NAME=form['timerTask_name']):
            return HttpResponse(JsonResponse({"resultCode":"0001","resultDesc":"NAME已经存在，名称不能重复！"}), content_type="application/json;charset=UTF-8")
        startTime=form["timerTask_startTime"]
        expiresTime=form["timerTask_expiresTime"]
        crontab_time=None
        if startTime:
            list1=form["timerTask_startTime"].split(' ')
            print form
            list2=list1[0].split('-')
            list3=list1[1].split(':')
            crontab_time = {
                'month_of_year': int(list2[1]), # 月份
                'day_of_month': int(list2[2]), # 日期
                'hour': int(list3[0]), # 小时
                'minute':int(list3[1]) # 分钟
            }
        interval_time=None
        if form["timerTask_every"] and not form["timerTask_every"] == "0":
            interval_time={
                "every":int(form["timerTask_every"]),
                "period":form["timerTask_period"]
            }
        kwargs={
            "jobTempleteId":str(form["timerTask_jobTemplete"]),
            "createUserId":str(request.session['userId']),
            "createUserName":request.session['username'],
            "startUserId":str(request.session['userId']) if form["timerTask_isUse"]=='true' else None,
            "startUserName":request.session['username'] if form["timerTask_isUse"]=='true' else None,
            "OWNER_ID":OWNER_ID,
            "OWNER_NAME":OWNER_NAME,
            "OWNER_PROJECT_ID":OWNER_PROJECT_ID,
            "OWNER_ALL":OWNER_ALL
        }
        log.info("kwargs :"+str(kwargs) )
        log.info("interval_time :"+str(interval_time) )
        log.info("crontab_time :"+str(crontab_time) )
        crontab=None
        if crontab_time:
            crontab = celery_models.CrontabSchedule.objects.filter(**crontab_time).first()
            if crontab is None:
                # 如果没有就创建，有的话就继续复用之前的crontab
                crontab = celery_models.CrontabSchedule.objects.create(**crontab_time)
        interval=None
        if interval_time:
            interval = celery_models.IntervalSchedule.objects.filter(**interval_time).first()
            if interval is None:
                # 如果没有就创建，有的话就继续复用之前的crontab
                interval = celery_models.IntervalSchedule.objects.create(**interval_time)

        #开启事物管理
        with transaction.atomic():
            timer_task=TimerTask(NAME=form["timerTask_name"],DESCRIPTION=form["timerTask_desc"],JOBTEMPLETE_ID=T_JOB_TEMPLATE.objects.get(id=form["timerTask_jobTemplete"]),ISUSE=True if form["timerTask_isUse"]=='true' else False,START_TIME=startTime if startTime else None,EXPIRES_TIME=expiresTime if expiresTime else None,EVERY=int(form["timerTask_every"]) if form["timerTask_every"] and not form["timerTask_every"]=="0"  else None,
                      PERIOD=form["timerTask_period"],OWNER_ID=OWNER_ID,OWNER_NAME=OWNER_NAME,OWNER_PROJECT_ID=OWNER_PROJECT_ID,OWNER_ALL=OWNER_ALL,CREATE_USER_ID=userId,CREATE_USER_NAME=userName)
            if form["timerTask_isUse"]=='true':
                task, created = celery_models.PeriodicTask.objects. get_or_create(name=form["timerTask_name"],task="app_tower.tasks.timer_task",crontab=crontab,interval=interval,enabled=True if form["timerTask_isUse"]=='true' else False,
                                                                                  kwargs=json.dumps(kwargs),expires=expiresTime,description=form["timerTask_desc"])
                task.save()
                timer_task.PERIODICTASK_ID  =  task

            timer_task.save()
        log.info("timerTask_add end" )
        return HttpResponse(json.dumps({'resultCode': '0000','resultDesc':'添加成功'}))
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        return HttpResponse(json.dumps({'resultCode': '0001','resultDesc':e.__str__()}))

@PermissionVerify()
def timerTask_select(request):
    log.info("timerTask_select start" )
    log.info("request: "+str(request))
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
        name = ''
        description = ''
        if request.GET.get("name"):
            name=request.GET.get("name")
        if request.GET.get("description"):
            description=request.GET.get("description")

        # 排序字段
        # ordername= request.GET.get('ordername')
        # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM     Test.objects.filter(name="runoob").order_by("id")
        timertaskList = TimerTask.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description).order_by(orderBy)
        total=len(timertaskList)


        list = timertaskList[int(offset):int(offset)+int(limit)]
        #[5:10]这是查找从下标5到下标10之间的数据，不包括10。


        response_data = {}

        response_data['resultCode'] = '0000'
        #序列码 serializers.serialize，且ensure_ascii=False防止乱码
        response_data['rows'] = serializers.serialize('json', list,ensure_ascii=False)
        response_data['total'] = total
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        return HttpResponse(json.dumps({'resultCode': '0001','resultDesc':e.__str__()}))
    log.info("timerTask_select end" )
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

@PermissionVerify()
def timerTask_delete(request):
    log.info('timerTask_delete start')
    log.info("request: "+str(request))
    form = {}
    if request.POST:
        form['id'] = request.POST['id']
        log.info("id:"+form['id'])
    # 删除id=1的数据
    if not TimerTask.objects.check_id(request,form['id']):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"定时任务没有使用权限！"}))
    timer_task = TimerTask.objects.get(id=form['id'])
    response_data = {}
    try:
        #开启事物管理
        with transaction.atomic():
            timer_task.delete()
            if timer_task.PERIODICTASK_ID:
                timer_task.PERIODICTASK_ID.delete()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '删除成功！'
    except Exception,ex:
        traceback.print_exc()
        log.error(ex)
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = ex.__str__()
    log.info('timerTask_delete end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

@PermissionVerify()
def timerTask_update(request):
    log.info('timerTask_update start')
    log.info('request:'+str(request))
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    response_data = {}
    try:
        form={}
        form['id']=request.POST["id"]
        if not TimerTask.objects.check_id(request,form['id']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"定时任务没有使用权限！"}))
        form["timerTask_name"]=request.POST["NAME"]
        form["timerTask_desc"]=request.POST["DESCRIPTION"]
        form["timerTask_jobTemplete"]=request.POST["JOBTEMPLETE_ID"]
        if not T_JOB_TEMPLATE.objects.check_id(request,form["timerTask_jobTemplete"]):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"任务模板没有使用权限！"}))
        form["timerTask_isUse"]=request.POST["ISUSE"]
        form["timerTask_startTime"]=request.POST["START_TIME"]
        form["timerTask_every"]=request.POST["EVERY"]
        if form["timerTask_startTime"]  and  form["timerTask_every"] :
            return HttpResponse(json.dumps({"resultCode":"0001","resultDesc":"开始时间和间隔时间二选一！"}))
        form["timerTask_period"]=request.POST["PERIOD"]
        form["timerTask_expiresTime"]=request.POST["EXPIRES_TIME"]
        form["timerTask_owner"]=request.POST["OWNER"]
        if form['timerTask_owner']=='onlyOne':
            OWNER_ID=request.session['userId']
            OWNER_NAME=request.session['username']
        elif form['timerTask_owner']=='all':
            OWNER_ALL=True
        else:
            if not T_PROJECT.objects.check_id(request,form['timerTask_owner']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"项目组没有使用权限！"}))
            OWNER_PROJECT_ID=form['timerTask_owner']
        userName=request.session['username']
        userId=request.session['userId']
        if TimerTask.objects.filter(NAME=request.POST['NAME']).exists():
            if not TimerTask.objects.get(NAME=request.POST['NAME']).id == int(request.POST['id']):
                response_data['resultCode']='0001'
                response_data['resultDesc']='NAME已经存在，名称不能重复！'
                return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")
        startTime=form["timerTask_startTime"].replace('T',' ')
        expiresTime=form["timerTask_expiresTime"].replace('T',' ')
        crontab_time=None
        if startTime:
            print startTime
            list1=startTime.split(' ')
            print form
            list2=list1[0].split('-')
            list3=list1[1].split(':')
            crontab_time = {
                'month_of_year': int(list2[1]), # 月份
                'day_of_month': int(list2[2]), # 日期
                'hour': int(list3[0]), # 小时
                'minute':int(list3[1]) # 分钟
            }
        interval_time=None
        if form["timerTask_every"] and not form["timerTask_every"] == "0":
            interval_time={
                "every":int(form["timerTask_every"]),
                "period":form["timerTask_period"]
            }
        kwargs={
            "jobTempleteId":str(form["timerTask_jobTemplete"]),
            "createUserId":str(request.session['userId']),
            "createUserName":request.session['username'],
            "startUserId":str(request.session['userId']) if form["timerTask_isUse"]=='true' else None,
            "startUserName":request.session['username'] if form["timerTask_isUse"]=='true' else None,
            "OWNER_ID":OWNER_ID,
            "OWNER_NAME":OWNER_NAME,
            "OWNER_PROJECT_ID":OWNER_PROJECT_ID,
            "OWNER_ALL":OWNER_ALL
        }
        crontab=None
        if crontab_time:
            crontab = celery_models.CrontabSchedule.objects.filter(**crontab_time).first()
            if crontab is None:
                # 如果没有就创建，有的话就继续复用之前的crontab
                crontab = celery_models.CrontabSchedule.objects.create(**crontab_time)
        interval=None
        if interval_time:
            interval = celery_models.IntervalSchedule.objects.filter(**interval_time).first()
            if interval is None:
                # 如果没有就创建，有的话就继续复用之前的crontab
                interval = celery_models.IntervalSchedule.objects.create(**interval_time)

        timer_task=TimerTask.objects.get(id=request.POST['id'])
        timer_task.NAME=form["timerTask_name"]
        timer_task.DESCRIPTION=form["timerTask_desc"]
        timer_task.JOBTEMPLETE_ID=T_JOB_TEMPLATE.objects.get(id=form["timerTask_jobTemplete"])
        timer_task.ISUSE=True if form["timerTask_isUse"]=='true' else False
        timer_task.START_TIME=startTime if startTime else None
        timer_task.EXPIRES_TIME=expiresTime if expiresTime else None
        timer_task.EVERY=int(form["timerTask_every"]) if form["timerTask_every"] and not form["timerTask_every"]=="0"  else None
        timer_task.PERIOD=form["timerTask_period"]
        timer_task.OWNER_ID=OWNER_ID
        timer_task.OWNER_NAME=OWNER_NAME
        timer_task.OWNER_PROJECT_ID=OWNER_PROJECT_ID
        timer_task.OWNER_ALL=OWNER_ALL
        timer_task.CREATE_USER_ID=userId
        timer_task.CREATE_USER_NAME=userName

        #开启事物管理
        with transaction.atomic():
            if timer_task.PERIODICTASK_ID :

                periodictaskid=timer_task.PERIODICTASK_ID_id
                timer_task.PERIODICTASK_ID_id=None
                celery_models.PeriodicTask.objects.get(id=periodictaskid).delete()
            if  form["timerTask_isUse"]=='true':
                task, created = celery_models.PeriodicTask.objects. get_or_create(name=form["timerTask_name"],task="app_tower.tasks.timer_task",crontab=crontab,interval=interval,enabled=True if form["timerTask_isUse"]=='true' else False,
                                                                                  kwargs=json.dumps(kwargs),expires=expiresTime,description=form["timerTask_desc"])
                task.save()
                timer_task.PERIODICTASK_ID=task

            timer_task.save()
        return HttpResponse(json.dumps({'resultCode': '0000','resultDesc':'修改成功'}))
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        return HttpResponse(json.dumps({'resultCode': '0001','resultDesc':e.__str__()}))

@PermissionVerify()
def timerTask_stop(request):
    log.info("timerTask_stop start")
    log.info("request: "+str(request))
    try:
         #开启事物管理
         with transaction.atomic():
             timerTaskId=request.POST['id']
             if not TimerTask.objects.check_id(request,request.POST['id']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"定时任务没有使用权限！"}))
             log.info("id :"+ request.POST['id'])
             timer_task=TimerTask.objects.get(id=timerTaskId)
             periodictaskid=timer_task.PERIODICTASK_ID_id
             timer_task.PERIODICTASK_ID_id=None
             timer_task.ISUSE=False
             celery_models.PeriodicTask.objects.get(id=periodictaskid).delete()
             timer_task.save()
         log.info("timerTask_stop end")
         return HttpResponse(json.dumps({'resultCode': '0000','resultDesc':'任务停止成功！'}))

    except Exception,e :
        traceback.print_exc()
        log.error(e.__str__())
        return HttpResponse(json.dumps({'resultCode': '0001','resultDesc':e.__str__()}))

@PermissionVerify()
def timerTask_start(request):
    log.info("timerTask_start start")
    log.info("request: "+str(request))
    try:
        timerTaskId=request.POST['id']
        log.info("id :"+ request.POST['id'])
        if not TimerTask.objects.check_id(request,request.POST['id']):
            return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"定时任务没有使用权限！"}))
        timer_task=TimerTask.objects.get(id=timerTaskId)
        print timer_task.START_TIME
        startTime=None
        if timer_task.START_TIME:
            startTime=str(timer_task.START_TIME).replace('T',' ')
        expiresTime=str(timer_task.EXPIRES_TIME).replace('T',' ')
        every=timer_task.EVERY
        period=timer_task.PERIOD
        crontab_time=None
        if startTime:
            list1=startTime.split(' ')
            list2=list1[0].split('-')
            list3=list1[1].split(':')
            crontab_time = {
                'month_of_year': int(list2[1]), # 月份
                'day_of_month': int(list2[2]), # 日期
                'hour': int(list3[0]), # 小时
                'minute':int(list3[1]) # 分钟
            }
        interval_time=None
        if every and not every == 0:
            interval_time={
                "every":every,
                "period":period
            }
        kwargs={
            "jobTempleteId":str(timer_task.JOBTEMPLETE_ID_id),
            "createUserId":str(request.session['userId']),
            "createUserName":request.session['username'],
            "startUserId":str(request.session['userId']),
            "startUserName":request.session['username'],
            "OWNER_ID":timer_task.OWNER_ID,
            "OWNER_NAME":timer_task.OWNER_NAME,
            "OWNER_PROJECT_ID":timer_task.OWNER_PROJECT_ID,
            "OWNER_ALL":timer_task.OWNER_ALL
        }
        log.info("kwargs :"+str(kwargs) )
        log.info("interval_time :"+str(interval_time) )
        log.info("crontab_time :"+str(crontab_time) )
        crontab=None
        if crontab_time:
            crontab = celery_models.CrontabSchedule.objects.filter(**crontab_time).first()
            if crontab is None:
                # 如果没有就创建，有的话就继续复用之前的crontab
                crontab = celery_models.CrontabSchedule.objects.create(**crontab_time)
        interval=None
        if interval_time:
            interval = celery_models.IntervalSchedule.objects.filter(**interval_time).first()
            if interval is None:
                # 如果没有就创建，有的话就继续复用之前的crontab
                interval = celery_models.IntervalSchedule.objects.create(**interval_time)

        #开启事物管理
        with transaction.atomic():
            task, created = celery_models.PeriodicTask.objects. get_or_create(name=timer_task.NAME,task="app_tower.tasks.timer_task",crontab=crontab,interval=interval,enabled=True,
                                                                              kwargs=json.dumps(kwargs),expires=expiresTime,description=timer_task.DESCRIPTION)
            task.save()

            timer_task.ISUSE=True
            timer_task.PERIODICTASK_ID=task
            timer_task.save()
        log.info("timerTask_start end")
        return HttpResponse(json.dumps({'resultCode': '0000','resultDesc':'任务启用成功！'}))
    except Exception,e :
        traceback.print_exc()
        log.error(e.__str__())
        return HttpResponse(json.dumps({'resultCode': '0001','resultDesc':e.__str__()}))