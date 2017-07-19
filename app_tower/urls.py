# -*- coding: utf-8 -*
from django.conf.urls import patterns, include, url
from app_tower.mysqldb import inventoriesdb

urlpatterns = patterns('inventories',
                        url(r'^inventories/select$', inventoriesdb.inventories_select),
                        url(r'^inventories/add$', inventoriesdb.inventories_add),
)


#
# urlpatterns = patterns('select',
#                        url(r'^inventories/select$', inventoriesdb.inventories_select),
# )
