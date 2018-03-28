# /usr/bin/python2
# -*- coding:utf8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
#from vega.rolelist_permissionlist_init import rolelist_permission
from settings import ENVIRONMENT
#from vega.deleteLogsRegular import runTask
@csrf_protect
def index(request):
    context = {}
    context['index'] = 'this is index!'
    context['environment']=ENVIRONMENT
    # initClass=rolelist_permission()
    # initClass.init_role_user()

    return render(request, 'templates/pages/index3.html', context)

def main(request):
    context = {}
    context['USERNAME'] =request.session['username']
    context['PERMISSIONNAMELIST']=request.session['permissionsNamelist']
    context['environment']=ENVIRONMENT

    return render(request, 'templates/pages/main.html', context)

