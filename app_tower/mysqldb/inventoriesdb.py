# -*- coding: utf-8 -*
from app_tower.models import inventories
from django.http import HttpRequest,HttpResponse
from django.http import JsonResponse
from json import dumps
from django.core import serializers
from django.shortcuts import render
import json
# 数据库操作
def inventories_add(request):
    form = {}
    if request.POST:
        form['name'] = request.POST['name']
        form['description'] = request.POST['description']
    inventorie = inventories(name=form['name'],description=form['description'])
    inventorie.save()
    return render(request, 'templates/pages/inventories.html',form)

def inventories_select(request):
    #本页第一条数据下标
    offset= request.GET.get('offset')
    # 每页数量
    limit = request.GET.get('limit')
    # 排序asc，desc
    order= request.GET.get('order')
    # 排序字段
    # ordername= request.GET.get('ordername')
    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM     Test.objects.filter(name="runoob").order_by("id")
    total=len(inventories.objects.all())
    try:
        list = inventories.objects.all()[int(offset):int(offset)+int(limit)]
        #[5:10]这是查找从下标5到下标10之间的数据，不包括10。
    except Exception,ex:
        print Exception,ex
    response_data = {}
    try:
        response_data['result'] = 'Success'
        #序列码 serializers.serialize，且ensure_ascii=False防止乱码
        response_data['rows'] = serializers.serialize('json', list,ensure_ascii=False)
        response_data['total'] = total
    except:
        response_data['result'] = 'Ouch!'
        response_data['rows'] = 'Script has not ran correctly'
    return HttpResponse(JsonResponse(response_data), content_type="application/json;charset=UTF-8")


def inventories_delete(request):
    form = {}
    if request.POST:
        form['id'] = request.POST['id']
        form['name'] = request.POST['name']
    # 删除id=1的数据
    inventorie = inventories.objects.get(id=form['id'])
    inventorie.delete()
    return HttpResponse("<p>数据删除成功！</p>")