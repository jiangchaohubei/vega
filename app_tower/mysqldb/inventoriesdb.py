# -*- coding: utf-8 -*
from app_tower.models import T_Group,T_LOGIN_CREDENTIALS,T_HOST,T_GROUP_HOST_ID,T_PROJECT,playbook,T_SYSTEM
from django.db.models import Q
from django.http import StreamingHttpResponse
from pyexcel_xls import get_data
# 写excel数据 (xls)   pyexcel_xls 以 OrderedDict 结构处理数据
from collections import OrderedDict
from pyexcel_xls import save_data
from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
import traceback
from django.core import serializers
from django.db import  transaction
import json
import os
from django.db import models
import logging

log = logging.getLogger("inventoriesdb")  # 为loggers中定义的名称
from authority.permission import PermissionVerify


#description:添加主机组
#params: request.POST {"NAME":"test","DESCRIPTION":"test","group_owner":"onlyOne","VARIABLES":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def group_add(request):
    log.info('group_add start')
    log.info("request: "+str(request))
    form = {}
    response_data={}
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    try:
        if request.POST:
            form['name'] = request.POST['NAME']
            form['description'] = request.POST['DESCRIPTION']
            form['owner'] = request.POST['group_owner']
            form['variables'] = request.POST['VARIABLES']
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
        if T_Group.objects.filter(NAME=form['name']):
            response_data['resultCode']='0001'
            response_data['resultDesc']='NAME已经存在，名称不能重复！'
            return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")
        group = T_Group(NAME=form['name'], DESCRIPTION=form['description'], VARIABLES=form['variables'],OWNER_ID=OWNER_ID,OWNER_NAME=OWNER_NAME,OWNER_PROJECT_ID=OWNER_PROJECT_ID,OWNER_ALL=OWNER_ALL,
                        CREATE_USER_ID=request.session['userId'] ,CREATE_USER_NAME=request.session['username'])
        group.save()
        response_data['resultCode']='0000'
        response_data['resultDesc']='Success'
    except Exception, ex:
        print Exception, ex
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode']='0001'
        response_data['resultDesc']=ex.__str__()
	log.info('group_add end')	
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

#创建回滚主机组
@PermissionVerify()
def create_backGroup(request):
    log.info("create_backGroup start")
    log.info("request: "+str(request))
    response_data={}
    try:
        hostIdList = request.POST.getlist('hostList[]');
        name=request.POST['name']
        desc=request.POST['desc']
        vars=request.POST['vars']
        owner=request.POST['owner']
        OWNER_ID=None
        OWNER_NAME=None
        OWNER_PROJECT_ID=None
        OWNER_ALL=False
        if owner=='onlyOne':
            OWNER_ID=request.session['userId']
            OWNER_NAME=request.session['username']
        elif owner=='all':
            OWNER_ALL=True
        else:
            if not T_PROJECT.objects.check_id(request,owner):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"项目组没有使用权限！"}))
            OWNER_PROJECT_ID=owner
        if T_Group.objects.filter(NAME=name):
            response_data['resultCode']='0001'
            response_data['resultDesc']='NAME已经存在，名称不能重复！'
            return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")
        #开启事物管理
        with transaction.atomic():
            t_group = T_Group(NAME=name, DESCRIPTION=desc, VARIABLES=vars,CREATE_USER_ID=request.session['userId'] ,CREATE_USER_NAME=request.session['username'],
                              OWNER_ID=OWNER_ID,OWNER_NAME=OWNER_NAME,OWNER_PROJECT_ID=OWNER_PROJECT_ID,OWNER_ALL=OWNER_ALL,)

            t_group.save()

            for hostId in hostIdList:
                    t_host=T_HOST.objects.get(id=int(hostId))
                    group_host = T_GROUP_HOST_ID(GROUP_ID=t_group, HOST_ID=t_host)
                    group_host.save()

        true = True
        false=False
        null = None
        groups=T_Group.objects.check_own(request)
        groupList = serializers.serialize('json', groups, ensure_ascii=False)
        credentials=T_LOGIN_CREDENTIALS.objects.check_own(request)
        credentialsList=serializers.serialize('json', credentials, ensure_ascii=False)
        projects=T_PROJECT.objects.check_own(request)
        projectList=serializers.serialize('json', projects, ensure_ascii=False)
        playbooks=playbook.objects.check_own(request)
        playbooksList=serializers.serialize('json', playbooks, ensure_ascii=False)

        response_data['resultCode']='0000'
        response_data['resultDesc']='Success'
        response_data['groupList']=groupList
        response_data['credentialsList']=credentialsList
        response_data['projectList']=projectList
        response_data['playbooksList']=playbooksList
    except  Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode']='0001'
        response_data['resultDesc']=e.__str__()

    log.info("create_backGroup end")
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:查询主机组
#params: request.GET {"limit":5,"offset":0,"order":"asc","ordername":"id","name":"","description":""}
#return: {"resultCode":"","resultDesc":"","rows":"","total":""}
@PermissionVerify()
def group_select(request):
    log.info('group_select start')
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
        if request.GET.get("name"):
            name = request.GET.get("name")
        if request.GET.get("description"):
            description = request.GET.get("description")
        # 排序字段
        # ordername= request.GET.get('ordername')
        # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM     Test.objects.filter(name="runoob").order_by("id")
        t_group_List = T_Group.objects.check_own(request).filter(NAME__contains=name).filter(DESCRIPTION__contains=description).order_by(orderBy)
        total=len(t_group_List)

        list = t_group_List[int(offset):int(offset) + int(limit)]
        for l in list:
            l.TOTAL_HOSTS=l.HOSTS.count()
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

    log.info('group_select end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:删除主机组
#params: request.POST {"id":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def group_delete(request):
    log.info('group_delete start')
    log.info("request: "+str(request))
    form = {}
    if request.POST:
        form['id'] = request.POST['id']
        log.info("id:"+str(form['id']))
    # 删除id=1的数据
    if not T_Group.objects.check_id(request,form['id']):
        return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机组没有使用权限！"}))
    inventorie = T_Group.objects.get(id=int(form['id']))
    response_data = {}
    try:
        inventorie.delete()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '删除成功！'
    except Exception,ex:
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = '已被使用，禁止删除！'
    log.info('group_delete end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:修改主机组
#params: request.POST {"id":"","name":"test","description":"test","owner":"onlyOne","variables":""}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def group_update(request):
    log.info('group_update start')
    log.info("request: "+str(request))
    form = {}
    OWNER_ID=None
    OWNER_NAME=None
    OWNER_PROJECT_ID=None
    OWNER_ALL=False
    response_data = {}
    try:
        if request.POST:
            form['id'] = request.POST['id']
            if not T_Group.objects.check_id(request,form['id']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机组没有使用权限！"}))
            form['name'] = request.POST['name']
            form['description'] = request.POST['description']
            form['variables'] = request.POST['variables']
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
            if T_Group.objects.filter(NAME=form['name']).exists():
                if not T_Group.objects.get(NAME=form['name']).id == int(form['id']):
                    response_data['resultCode']='0001'
                    response_data['resultDesc']='NAME已经存在，名称不能重复！'
                    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")
            inventorie = T_Group.objects.get(id=form['id'])
            inventorie.NAME = form['name']
            inventorie.DESCRIPTION = form['description']
            inventorie.VARIABLES = form['variables']
            inventorie.MODIFY_USER_ID=request.session['userId']
            inventorie.OWNER_ID=OWNER_ID
            inventorie.OWNER_NAME=OWNER_NAME
            inventorie.OWNER_PROJECT_ID=OWNER_PROJECT_ID
            inventorie.OWNER_ALL=OWNER_ALL
            inventorie.save()
            response_data['resultCode'] = '0000'
            response_data['resultDesc'] = '修改成功！'
    except Exception,e:
        traceback.print_exc()
        log.error(e.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = e.__str__()
    log.info('group_update end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

# 导出主机组的信息 先查询主机组的信息 再写入到服务器上在 导出
#description:导出主机，程序列表
#params: request.POST
#return: {"resultCode":"","resultDesc":"","filepath":""}
@PermissionVerify()
def group_export(request):
    response_data = {}
    log.info('group_export start')
    try:
        # 查询
        groupList = T_Group.objects.all()
        # 写Excel数据, xls格式
        data = OrderedDict()
        # sheet表的数据
        sheet_1 = []
        row_1_data = [u"ID",u"组名称", u"描述"]  # 每一行的数据
        # 添加表头
        sheet_1.append(row_1_data)
        # 遍历  逐条添加数据
        for group in groupList:
            row_data=[]
            row_data.append(group.id)
            row_data.append(group.NAME)
            row_data.append(group.DESCRIPTION)
            sheet_1.append(row_data)
        # 添加sheet表
        data.update({u"这是组表": sheet_1})
        exportRoot = str(os.getcwd()) + "/export/write.xls"
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
    log.info('group_export end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


def group_download(request):
    response_data={}
    form={}
    log.info('group_download start')
    form["filepath"]=request.GET['filepath']
    form["filename_"]="主机组"
    form["filetype_"]=".xls"
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
    response['Content-Disposition'] = 'attachment; filename=' + form["filename_"] + form["filetype_"] # 设定传输给客户端的文件名称
    response['Content-Length'] = os.path.getsize(form["filepath"])  # 传输给客户端的文件大小
    log.info('group_download end')
    # 导出成功之后   删除服务器上的文件
    os.remove(form["filepath"])
    return response

#description:主机组添加host
#params: request.POST {"id":"groupId","hostList":"[]",}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
def host_add(request):
    log.info('host_add start')
    log.info("request: "+str(request))
    form = {}
    response_data={}
    try:
        if request.POST:
            form['id'] = request.POST['id']
            if not T_Group.objects.check_id(request,form['id']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机组没有使用权限！"}))
            form['hostList'] = request.POST['hostList']

            log.info("form:"+str(form))
        group = T_Group.objects.get(id=form['id'])
        #开启事物管理
        with transaction.atomic():
            for h in eval(form['hostList']):
                if not T_HOST.objects.filter(NAME=h).exists():
                    response_data['errorHost']=h
                host=T_HOST.objects.get(NAME=h)
                group_host,create = T_GROUP_HOST_ID.objects.get_or_create(GROUP_ID=group, HOST_ID=host)
                group_host.save()
        response_data['resultCode']='0000'
        response_data['resultDesc']='Success'
    except Exception, ex:
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode']='0001'
        response_data['resultDesc']=ex.__str__()
    log.info('host_add end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#   先将组文件上传到服务器上  再将组文件保存到数据库中
def hosts_import(request):
    log.info('hosts_import start')

    form = {}
    response_data={}
    importRoot=str(os.getcwd())+"/import"
    excelPath=""
    try:
        if request.method == "POST":  # 请求方法为POST时，进行处理
            log.info('hosts_upload start')
            form['id']=request.POST['uploadGroupId']
            if not T_Group.objects.check_id(request,form['id']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机组没有使用权限！"}))
            form['delete']=request.POST['delete']
            myFile = request.FILES.get("inputFile", None)  # 获取上传的文件，如果没有文件，则默认为None
            if not myFile:
                log.info("no files for upload!")
                response_data['resultCode'] = '0001'
                response_data['resultDesc'] = 'Faield'
            destination = open(os.path.join(importRoot, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in myFile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            log.info("hosts_upload over!")
            excelPath=importRoot+"/"+myFile.name
            xls_data = get_data(excelPath)
            if form['delete']=='true':
                group = T_Group.objects.get(id=form['id'])
                group.HOSTS.all().delete()

            for sheet_n in xls_data.keys():
                repeatHost=[]
                for host in xls_data[sheet_n][1:]:
                    if len(host)==2:
                        NAME = host[0]
                        DESCRIPTION = host[1]
                        VARIABLES=""

                    else:
                        NAME = host[0]
                        DESCRIPTION = host[1]
                        VARIABLES = host[2]
                    group = T_Group.objects.get(id=form['id'])
                    host = T_HOST(NAME=NAME, DESCRIPTION=DESCRIPTION,VARIABLES=VARIABLES,OWNER_ALL=group.OWNER_ALL,OWNER_PROJECT_ID=group.OWNER_PROJECT_ID,CREATE_USER_ID=request.session['userId'] ,CREATE_USER_NAME=request.session['username'])

                    host_list=group.HOSTS.all()
                    hostList = serializers.serialize('json', host_list, ensure_ascii=False)
                    true = True
                    false=False
                    null = None
                    host_list_dic=eval(hostList)
                    goContinue=False

                    for h in host_list_dic:
                        if NAME==h['fields']['NAME']:
                            goContinue=True
                            repeatHost.append(NAME)

                    if goContinue :
                        continue
                    host.save()
                    group_host = T_GROUP_HOST_ID(GROUP_ID=group, HOST_ID=host)
                    group_host.save()

            # 上传成功之后删除文件
            os.remove(excelPath)
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = {'SUCCESS':'true','repeatHost':repeatHost}
    except Exception, ex:
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = ex.__str__()
    log.info('hosts_import end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


#description:查询主机组中host
#params: request.GET {"limit":5,"offset":0,"order":"asc","ordername":"id","id":"groupId"}
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
        id = request.GET.get('id')
        # 排序字段
        # ordername= request.GET.get('ordername')
        group = T_Group.objects.get(id=id)
        ##多对多的查询##
        hostlist = group.HOSTS.all().order_by(orderBy)
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

#description:删除主机组中主机（解除绑定关系）
#params: request.POST {"id":"hostId","groupId":"groupId"}
#return: {"resultCode":"","resultDesc":""}
@PermissionVerify()
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
            form['groupId'] = request.POST['groupId']
            if not T_Group.objects.check_id(request,form['groupId']):
                return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机组没有使用权限！"}))
        # 删除id=1的数据
        host = T_HOST.objects.get(id=form['id'])
        group = T_Group.objects.get(id=form['groupId'])
        T_GROUP_HOST_ID.objects.filter(GROUP_ID=group,HOST_ID=host).delete()
        response_data['resultCode'] = '0000'
        response_data['resultDesc'] = '删除成功！'
    except Exception, ex:
        print Exception, ex
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = ex.__str__()
    log.info('host_delete end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


# # 组根据id更新
# @PermissionVerify()
# def host_update(request):
#     log.info('host_update start')
#     log.info("request: "+str(request))
#     form = {}
#     response_data = {}
#     try:
#         if request.POST:
#             form['id'] = request.POST['id']
#             if not T_HOST.objects.check_id(request,form['id']):
#                 return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机没有使用权限！"}))
#             form['groupId'] = request.POST['groupId']
#             if not T_Group.objects.check_id(request,form['groupId']):
#                 return HttpResponse(json.dumps({"resultCode":"0057","resultDesc":"主机组没有使用权限！"}))
#             form['name'] = request.POST['name']
#             form['description'] = request.POST['description']
#             form['variables'] = request.POST['variables']
#             log.info("form:"+str(form))
#         host = T_HOST.objects.get(id=form['id'])
#         host.NAME = form['name']
#         host.DESCRIPTION = form['description']
#         host.VARIABLES = form['variables']
#         host.MODIFY_USER_ID=request.session['userId']
#         group=T_Group.objects.get(id=form['groupId'])
#         host_list=group.HOSTS.all()
#         hostList = serializers.serialize('json', host_list, ensure_ascii=False)
#         true = True
#         false=False
#         null = None
#         host_list_dic=eval(hostList)
#         for h in host_list_dic:
#             if not h['pk']==int(form['id']):
#                 if form['name']==h['fields']['NAME']:
#                     response_data['resultCode']='0001'
#                     response_data['resultDesc']='主机已经存在，不能重复！'
#                     return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")
#
#         host.save()
#         response_data['resultCode'] = '0000'
#         response_data['resultDesc'] = '成功'
#     except Exception, ex:
#         print Exception, ex
#         traceback.print_exc()
#         log.error(ex.__str__())
#         response_data['resultCode'] = '0001'
#         response_data['resultDesc'] = ex.__str__()
#     log.info('host_update end')
#     return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")



def downloadXLSX(request):
    # do something...
    log.info('downloadXLSX start')
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    file_name=request.GET.get('filename')
    #format_file_name=""
    # if file_name=='host.xlsx':
    #     format_file_name='host.xlsx'
    # elif   file_name=='instructions.pptx':
    #     format_file_name='host.xlsx'
    # elif    file_name=='host.docx':
    #     format_file_name='host.xlsx'
    the_file_name = str(os.getcwd())+"/static/doc/"+file_name
    log.info(the_file_name)
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    log.info('downloadXLSX end')
    return response

def searchHostByGrooupId(request):
    response_data = {}
    groupId=request.POST['groupId']
    group=T_Group.objects.get(id=int(groupId))
    host_list=group.HOSTS.all()
    hostList = serializers.serialize('json', host_list, ensure_ascii=False)
    true = True
    false=False
    null = None
    host_list_dic=eval(hostList)
    response_data['hostList']= host_list_dic
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

def selectBySomething(request):
    log.info('selectBySomething end')
    response_data = {}
    try:
        system_id=request.POST['system_id']
        keyword=''
        if request.POST['keyword']:
            keyword = request.POST['keyword']
        if system_id=='all':
            t_host_List = T_HOST.objects.check_own(request).filter(Q(NAME__contains=keyword) | Q(DESCRIPTION__contains=keyword))
        else:
            t_host_List = T_HOST.objects.check_own(request).filter(Q(NAME__contains=keyword) | Q(DESCRIPTION__contains=keyword),SYSTEM_ID_id=system_id)

        hostList = serializers.serialize('json', t_host_List, ensure_ascii=False)
        true = True
        false=False
        null = None
        host_list_dic=eval(hostList)
        response_data['resultCode']='0000'
        response_data['resultDesc']='查询成功'
        response_data['hostList']= host_list_dic
    except Exception, ex:
        print Exception, ex
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = ex.__str__()
    log.info('selectBySomething end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")

def init_cmdb_system(request):
    log.info('init_cmdb_system end')
    response_data = {}
    try:

        system=T_SYSTEM.objects.check_own(request)
        systemList = serializers.serialize('json', system, ensure_ascii=False)
        true = True
        false=False
        null = None
        system_list_dic=eval(systemList)
        response_data['resultCode']='0000'
        response_data['resultDesc']='查询成功'
        response_data['systemList']= system_list_dic
    except Exception, ex:
        print Exception, ex
        traceback.print_exc()
        log.error(ex.__str__())
        response_data['resultCode'] = '0001'
        response_data['resultDesc'] = ex.__str__()
    log.info('init_cmdb_system end')
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")
