# -*- coding: utf-8 -*
from app_tower.models import jobTemplate
from django.http import HttpResponse
import json
# 数据库操作
def jobTemplate_add(request):
    form = {}
    if request.POST:
        form['name'] = request.POST['name']
        form['description'] = request.POST['description']
    job = jobTemplate(name=form['name'],description=form['description'])
    job.save()
    return HttpResponse("<p>数据添加成功！</p>")

def jobTemplate_select(request):
    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    list = jobTemplate.objects.all()
    list_json=json.dumps(list)
    print list_json
    return list_json

def jobTemplate_selectById(request):
    form = {}
    if request.POST:
        form['id'] = request.POST['id']
    job=jobTemplate.objects.get(id=form['id'])
    return job

def jobTemplate_delete(request):
    form = {}
    if request.POST:
        form['id'] = request.POST['id']
        form['name'] = request.POST['name']
    # 删除id=1的数据
    job = jobTemplate.objects.get(id=form['id'])
    job.delete()
    return HttpResponse("<p>数据删除成功！</p>")

def jobTemplate_run(request):
    form = {}
    if request.POST:
        form['id'] = request.POST['id']
        form['name'] = request.POST['name']
    # 删除id=1的数据
    job = jobTemplate.objects.get(id=form['id'])
    job.delete()
    return HttpResponse("<p>数据删除成功！</p>")