# -*- coding: utf-8 -*
from django.conf.urls import patterns, include, url
from app_cmdb.mysqldb import hostdb,systemdb,moduledb,softwaredb,versiondb


urlpatterns = patterns('app_cmdb',
                        url(r'^host/add$', hostdb.host_add),
                        url(r'^host/select$', hostdb.host_select),
                        url(r'^host/delete$', hostdb.host_delete),
                        url(r'^host/update$', hostdb.host_update),
                        url(r'^host/export$', hostdb.host_export),
                        url(r'^host/export/download$', hostdb.host_download),


                       url(r'^system/add$', systemdb.system_add),
                       url(r'^system/select$', systemdb.system_select),
                       url(r'^system/delete$', systemdb.system_delete),
                       url(r'^system/update$', systemdb.system_update),
                       url(r'^system/init_system_select$', systemdb.init_system_select),
                       url(r'^system/export$', systemdb.system_export),
                       url(r'^system/export/download$', systemdb.system_download),
                       url(r'^system/import$', systemdb.system_import),

                       url(r'^module/add$', moduledb.module_add),
                       url(r'^module/select$', moduledb.module_select),
                       url(r'^module/delete$', moduledb.module_delete),
                       url(r'^module/unwarp$', moduledb.module_unwarp), ##解绑
                       url(r'^module/update$', moduledb.module_update),
                       url(r'^module/init_module_select$', moduledb.init_module_select),

                       url(r'^software/add$', softwaredb.software_add),
                       url(r'^software/select$', softwaredb.software_select),
                       url(r'^software/delete$', softwaredb.software_delete),
                       url(r'^software/update$', softwaredb.software_update),
                       url(r'^software/init_system_module_select$', softwaredb.init_system_module_select),
                       url(r'^software/host_add$', softwaredb.host_add),
                       url(r'^software/host_select$', softwaredb.host_select),
                       url(r'^software/host_delete$', softwaredb.host_delete),
                       url(r'^software/init_cmdb_system$', softwaredb.init_cmdb_system),

                       url(r'^version/add$', versiondb.version_add),
                       url(r'^version/select$', versiondb.version_select),
                       url(r'^version/delete$', versiondb.version_delete),



)



#
# urlpatterns = patterns('select',
#                        url(r'^inventories/select$', inventoriesdb.inventories_select),
# )
