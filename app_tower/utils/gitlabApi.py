#!/usr/bin/env python
# -*- coding:utf8 -*-
import urllib2
import json
import base64
import os
import cStringIO


#获取密钥
def get_private_token(login,password,ip):
    requesturl = urllib2.Request(ip+"/api/v3/session")
    requesturl.add_header('Content-Type', 'application/json')
    requesturl.add_header('cache-control', 'no-cache')
    try:
        #post请求传参
        response = urllib2.urlopen(requesturl,json.dumps({"login":login,"password":password}))
        resString = response.read().decode('utf-8')
        print resString
        true=True
        false=False
        null=None
        private_token=eval(resString)['private_token']
        print private_token
        return (True,private_token)
    except Exception as e:
        return (False,e.__str__())
#获取项目列表
def getOwn_projects(private_token,ip):
    requesturl = urllib2.Request(ip+"/api/v3/projects?private_token="+private_token)
    requesturl.add_header('Content-Type', 'application/json')
    requesturl.add_header('cache-control', 'no-cache')
    try:
        response = urllib2.urlopen(requesturl)
        true=True
        false=False
        null=None
        resString = response.read().decode('utf-8')
        return (True,eval(resString))
    except Exception,e:
        return (False,e.__str__())


#获取项目文件tree
def get_project_tree(id,private_token,ip,path=""):
    print 'test_get_project_tree'
    try:
        requesturl = urllib2.Request(ip+"/api/v3/projects/"+id+"/repository/tree?private_token="+private_token+"&path="+path)
        requesturl.add_header('Content-Type', 'application/json')
        requesturl.add_header('cache-control', 'no-cache')
        response = urllib2.urlopen(requesturl)
        resString = response.read().decode('utf-8')
        true=True
        false=False
        null=None
        print resString
        return (True,eval(resString))
    except Exception,e:
        return (False,e.__str__())
#下载项目压缩包
def download_projectgz(id,name,private_token,ip):
    print 'test_download'
    try:
        requesturl = urllib2.Request(ip+"/api/v3/projects/"+id+"/repository/archive?private_token="+private_token)
        requesturl.add_header('Content-Type', 'application/json')
        requesturl.add_header('cache-control', 'no-cache')
        response = urllib2.urlopen(requesturl)
        f = cStringIO.StringIO(response.read())
        destination = open(os.path.join("C:\Users\PC\Downloads\\", name+".tar.gz"), 'wb+')  # 打开特定的文件进行二进制的写操作

        destination.write(f.read())
        destination.close()
        #str = response.read().decode('utf-8')

        return (True,"download complete")
    except Exception,e:
        return (False,e.__str__())

#获取文件内容
def read_fileContent(id,private_token,filepath,ip):
    print 'test_download'
    try:
        requesturl = urllib2.Request(ip+"/api/v3/projects/"+id+"/repository/blobs/master?private_token="+private_token+"&filepath="+filepath)
        requesturl.add_header('Content-Type', 'application/json')
        requesturl.add_header('cache-control', 'no-cache')
        response = urllib2.urlopen(requesturl)
        resString = response.read().decode('utf-8')

        return (True,resString)
    except Exception,e:
        return (False,e.__str__())