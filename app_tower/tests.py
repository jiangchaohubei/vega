# /usr/bin/python2
# -*- coding:utf8 -*-
from django.test import TestCase
#from app_tower.tasks import add,sendmail
import time
#from celery.task.control import revoke
import logging
log = logging.getLogger("test1") # 为loggers中定义的名称
# Create your tests here.
import urllib2
import json
import base64
import os
import cStringIO
class celery_test(TestCase):
    def test_get_private_token(self):
        request = urllib2.Request("http://180.168.71.6:8000/api/v3/session")
        request.add_header('Content-Type', 'application/json')
        request.add_header('cache-control', 'no-cache')
        try:
            response = urllib2.urlopen(request,json.dumps({"login":"jiangchao_hubei","email":"jiangchao_hubei@126.com","password":"jc199310081121"}))

            print response
            resString = response.read().decode('utf-8')
            print resString
            true=True
            false=False
            null=None
            private_token=eval(resString)['private_token']
            print private_token
            self.test_getOwn_project(private_token)
        except Exception,e:
            print e

    def test_getOwn_project(self,private_token):
        request = urllib2.Request("http://180.168.71.6:8000/api/v3/projects?private_token="+private_token)
        request.add_header('Content-Type', 'application/json')
        request.add_header('cache-control', 'no-cache')
        response = urllib2.urlopen(request)
        true=True
        false=False
        null=None
        resString = response.read().decode('utf-8')
        name= eval(resString)[1]['name']
        id=eval(resString)[1]['id']
        print id,name
        #self.test_download(str(id),name,private_token)
        self.test_get_project_tree(str(id),name,private_token)

        print 'end'

    def test_get_project_tree(self,id,name,private_token):
        print 'test_get_project_tree'
        try:
            request = urllib2.Request("http://180.168.71.6:8000/api/v3/projects/"+id+"/repository/tree?private_token="+private_token+"&path=routes")
            request.add_header('Content-Type', 'application/json')
            request.add_header('cache-control', 'no-cache')
            response = urllib2.urlopen(request)

            resString = response.read().decode('utf-8')
            print resString

            print "end"
        except Exception,e:
            print e

    def test_download(self,id,name,private_token):
        print 'test_download'
        try:
            #request = urllib2.Request("http://180.168.71.6:8000/api/v3/projects/"+id+"/repository/blobs/master?private_token="+private_token+"&filepath=app.js")
            request = urllib2.Request("http://180.168.71.6:8000/api/v3/projects/"+id+"/repository/archive?private_token="+private_token)
            request.add_header('Content-Type', 'application/json')
            request.add_header('cache-control', 'no-cache')
            response = urllib2.urlopen(request)
            f = cStringIO.StringIO(response.read())
            destination = open(os.path.join("C:\Users\PC\Downloads\\", name+".tar.gz"), 'wb+')  # 打开特定的文件进行二进制的写操作

            destination.write(f.read())
            destination.close()
            #str = response.read().decode('utf-8')

            print "end"
        except Exception,e:
            print e





