# -*- coding: utf-8 -*-
"""
 功能： 记录用户操作记录
 说明： Django中间件
 修订： v2.0
"""
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth import SESSION_KEY
from urllib import quote
from  vega.permission_config import permissionList
import json
from app_tower.models import operation_record
from django.http.request import RawPostDataException
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
# 不需要拦截的请求
FILTER_URL = ['/index', '/authority/user/select/capcha', '/authority/user/login', '/login',
              '/authority/user/checkUserName','/authority/user/check/capcha','/authority/user/checkUserQuestion',
              '/authority/user/loginCapcha','/authority/user/reset/password/mobile',
              '/authority/user/reset/password/email']
class recordMiddleware(object):

    urlList=[]
    for pname ,list in permissionList.items():
        urlList+=list
    def process_request(self, request):
        response = HttpResponse()
        req_path = request.path
        if req_path == "/":
            response.write("<script>top.location.href='/login'</script>")
            return response

        if req_path not in FILTER_URL:
            if 'static' not in req_path:
                username = request.session.get("username", '')
                if username == '':
                    # 这里要跳出整个frameset
                    jump_to_console = "<script>alert('抱歉，会话过期，请登录系统！');top.location.href='/login'</script>"
                    response = HttpResponse(jump_to_console)
                    print req_path
                    if req_path =="/main" or req_path =='/authority/user/logout/':
                        return response
                    else:
                        return  HttpResponse(JsonResponse({"resultCode":"0087","resultDesc":u"抱歉，会话过期，请登录系统！"}), content_type="application/json;charset=UTF-8")
                        # return HttpResponseRedirect("/index")
                    # return HttpResponseRedirect("/index")
    def process_view(self, request, view, args, kwargs) :
        pass


    def  process_response(self, request, response) :
        req_path = request.path
        if req_path == "/"  :
            response.write("<script>top.location.href='/login'</script>")
            return response

        if req_path not in FILTER_URL:
            if 'static' not in req_path:
                username = request.session.get("username", '')
                if username == '':
                    # # 这里要跳出整个frameset
                    # response.write("<script>alert('抱歉，会话过期，请登录系统！');top.location.href='/login'</script>")
                    # return response
                    #通过js来跳转页面，取巧
                    jump_to_console = "<script>alert('抱歉，会话过期，请登录系统！');top.location.href='/login'</script>"
                    response = HttpResponse(jump_to_console)
                    print req_path
                    if req_path =="/main" or req_path =='/authority/user/logout/':
                        return response
                    else:
                        return  HttpResponse(JsonResponse({"resultCode":"0087","resultDesc":u"抱歉，会话过期，请登录系统！"}), content_type="application/json;charset=UTF-8")
                        # return HttpResponseRedirect("/index")
        for ul in recordMiddleware.urlList:
            if req_path==ul['url'] :
                if ul['name']=='updateSudo':
                    print request.POST
                    # bodyList=str(request.body).split('&')
                    # print bodyList
                    OPERATION_IP=request.POST['hostList']
                    OPERATION_PORT=request.POST['port']
                    OPERATION_ACCOUNT=request.POST['userName']
                    OPERATION_ACTION=request.POST['action']
                    requestUser=request.POST['requestUser']
                    OPERATION_DESCRIPTION=""
                    if OPERATION_ACTION=='add':
                        OPERATION_DESCRIPTION+="应("+requestUser+")要求增加sudo权限"
                    if OPERATION_ACTION=='cancel':
                        OPERATION_DESCRIPTION+="应("+requestUser+")要求取消sudo权限"
                    if OPERATION_ACTION=='search':
                        OPERATION_DESCRIPTION+="应("+requestUser+")要求查询sudo权限"
                    if OPERATION_ACTION=='searchFile':
                        OPERATION_DESCRIPTION+="应("+requestUser+")要求查询sudoer文件"

                    record=operation_record(NAME=ul['cname'],PERMISSION_NAME=ul['name'],URL=ul['url'],REQUEST=str(request),REQUEST_BODY=str(request.body),RESPONSE_CONTENT=str(response.content),
                                            CREATE_USER_ID=request.session['userId'],CREATE_USER_NAME=request.session['username'],OPERATION_IP=OPERATION_IP,OPERATION_PORT=OPERATION_PORT,OPERATION_ACCOUNT=OPERATION_ACCOUNT,
                                            OPERATION_ACTION=OPERATION_ACTION,OPERATION_DESCRIPTION=OPERATION_DESCRIPTION)
                else :
                    bodyStr=""
                    contentStr=""
                    try:
                        bodyStr=str(request.body)
                    except RawPostDataException,e:
                        bodyStr=None
                    try:
                        contentStr=str(response.content)
                    except RawPostDataException,e:
                        contentStr=None
                    record=operation_record(NAME=ul['cname'],PERMISSION_NAME=ul['name'],URL=ul['url'],REQUEST=str(request),REQUEST_BODY=bodyStr,RESPONSE_CONTENT=contentStr,
                                     CREATE_USER_ID=request.session['userId'],CREATE_USER_NAME=request.session['username'])
                record.save()
        return   response