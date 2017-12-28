# -*- coding: utf-8 -*
from app_tower.models import T_JOB,T_JOB_TEMPLATE,T_Group,T_LOGIN_CREDENTIALS,T_PROJECT,playbook
import json
from django.http import HttpRequest,HttpResponse
from django.http import JsonResponse
from app_tower.models import User
from django.core import serializers
import traceback
import logging
log = logging.getLogger("jobsdb")
from authority.permission import PermissionVerify

#查询任务
#params: request.GET {"limit":5,"offset":0,"order":"asc","ordername":"id","name":"","description":"","jobTaskid":"","jobType":"","jobStatus":""}
#return: {"resultCode":"","resultDesc":"","rows":"","total":""}
@PermissionVerify()
def jobs_select(request):
    log.info('jobs_select start')
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
        ordername=ordername.replace('fields.','')
        orderBy=order+ordername
        name = ''
        description = ''
        jobType=''
        jobTaskid=''
        jobStatus=''
        if request.GET.get("name"):
            name=request.GET.get("name")
        if request.GET.get("description"):
            description=request.GET.get("description")
        if request.GET.get('jobTaskid'):
            jobTaskid=request.GET.get("jobTaskid")

        if request.GET.get('jobType')!="-1":
            jobType=request.GET.get("jobType")
        if request.GET.get('jobStatus')!="-1":
            jobStatus=request.GET.get("jobStatus")

        jobslist=T_JOB.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description). \
            filter(CELERY_TASK_ID__contains=jobTaskid).filter(JOB_TYPE__contains=jobType).filter(STATUS__contains=jobStatus).order_by(orderBy)
        total = len(jobslist)

        list = jobslist[int(offset):int(offset)+int(limit)]
            #[5:10]这是查找从下标5到下标10之间的数据，不包括10。

        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '查询成功！'
        #序列码 serializers.serialize，且ensure_ascii=False防止乱码
        response_data['rows'] = serializers.serialize('json', list,ensure_ascii=False)
        response_data['total'] = total
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()

    log.info('jobs_select end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#删除任务  数据库删除   根据id删除
#params: request.POST {"id":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def jobs_delete(request):
    log.info('jobs_delete start')
    log.info("request: "+str(request))
    form = {}
    try:
        if request.POST:
            form['id'] = request.POST['id']
            log.info("id:"+str(form))
            if not T_JOB.objects.check_id(request,form['id']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"任务没有使用权限！"}))
        # 根据id删除的数据
        job = T_JOB.objects.get(id=form['id'])
        job.delete()
        response_data = {}

        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '删除成功！'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    log.info('jobs_delete end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")




