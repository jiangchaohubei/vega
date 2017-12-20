# -*- coding: utf-8 -*
from django.test import TestCase
from mysqldb import hostdb,moduledb,softwaredb,systemdb,versiondb
from app_tower.models import User,RoleList,PermissionList,T_RoleList_PermissionList_ID,T_SYSTEM,T_HOST,T_MODULE,T_SOFTWARE,T_VERSION
from vega.rolelist_permissionlist_init import rolelist_permission
from authority.mysqldb.authoritydb import md5
# Create your tests here.

class hostdbTestCase(TestCase):
    def setUp(self):
        print("hostdbTestCase======in setUp")
        # initClass=rolelist_permission()
        # initClass.init_role_user()
        role,created=RoleList.objects.get_or_create(name=u"超级管理员")
        role.save()
        user ,created= User.objects.get_or_create(username='jzyuan',mobile='15001994524', password=md5("88888888"),email='jiangchao_hubei@163.com',nickname='jzyuan',is_superuser="1",role=RoleList.objects.get(name=u"超级管理员"))
        user.save()
        res=self.client.post('/authority/user/login',{"USERNAME":"jzyuan","PASSWORD":"88888888"})
        print res.content
        self.assertEqual(res.status_code,200)

    #测试主机添加
    def test_host_add(self):
        system = T_SYSTEM(NAME="应用中心", DESCRIPTION="test", COMPANY="test",OWNER_ALL=True)
        system.save()
        res=self.client.post('/app_cmdb/host/add',{"NAME":"10.200.86.172","DESCRIPTION":"test","VARIABLES":"","OWNER":"onlyOne","MACHINE_TYPE":"1","MACHINE_ROOM":"1",
                                                   "MACHINE_POSITION":"1","CUTTER_NUMBER":"1","SN_NUMBER":"1","OS":"1","PHYSICAL_MACHINE_TYPE":"1","NOTE":"1","SYSTEM_ID":system.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

    #测试主机查询
    def test_host_select(self):
        res=self.client.get('/app_cmdb/host/select',{"limit":5,"offset":0,"order":"asc","ordername":"id","systemId":"0"})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

    #测试主机删除
    def test_host_delete(self):

        host=T_HOST(NAME="10.200.86.172",DESCRIPTION="test",VARIABLES="",MACHINE_TYPE="1",MACHINE_ROOM="1",
                                       MACHINE_POSITION="1",CUTTER_NUMBER="1",SN_NUMBER="1",OS="1",PHYSICAL_MACHINE_TYPE="1",NOTE="1",OWNER_ALL=True)
        host.save()
        res=self.client.post('/app_cmdb/host/delete',{"id":host.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

    #测试主机修改
    def test_host_update(self):
        system = T_SYSTEM(NAME="应用中心", DESCRIPTION="test", COMPANY="test",OWNER_ALL=True)
        system.save()
        host=T_HOST(NAME="10.200.86.172",DESCRIPTION="test",VARIABLES="",MACHINE_TYPE="1",MACHINE_ROOM="1",
                    MACHINE_POSITION="1",CUTTER_NUMBER="1",SN_NUMBER="1",OS="1",PHYSICAL_MACHINE_TYPE="1",NOTE="1",OWNER_ALL=True)
        host.save()
        res=self.client.post('/app_cmdb/host/update',{"id":host.id,"NAME":"10.200.86.173","DESCRIPTION":"test","VARIABLES":"","OWNER":"onlyOne","MACHINE_TYPE":"1","MACHINE_ROOM":"1",
                                                   "MACHINE_POSITION":"1","CUTTER_NUMBER":"1","SN_NUMBER":"1","OS":"1","PHYSICAL_MACHINE_TYPE":"1","NOTE":"1","SYSTEM_ID":system.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

    # #测试主机导出xlsx
    # def test_host_export(self):
    #
    #     res=self.client.post('/app_cmdb/host/export',{"name":"","description":"","systemId":""})
    #     self.assertEqual(eval(res.content)['resultCode'],'0000')
    #     print eval(res.content)['resultDesc']
    #     return eval(res.content)['filepath']
    #
    # #测试主机xlsx下载
    # def test_host_download(self):
    #     filepath=self.test_host_export()
    #     res=self.client.get('/app_cmdb/host/export/download',{"filepath":filepath})
    #     print res.content


    def tearDown(self):
        print("hostdbTestCase======in tearDown")









class moduledbTestCase(TestCase):
    def setUp(self):
        print("moduledbTestCase======in setUp")
        # initClass=rolelist_permission()
        # initClass.init_role_user()
        role,created=RoleList.objects.get_or_create(name=u"超级管理员")
        role.save()
        user ,created= User.objects.get_or_create(username='jzyuan',mobile='15001994524', password=md5("88888888"),email='jiangchao_hubei@163.com',nickname='jzyuan',is_superuser="1",role=RoleList.objects.get(name=u"超级管理员"))
        user.save()
        res=self.client.post('/authority/user/login',{"USERNAME":"jzyuan","PASSWORD":"88888888"})
        print res.content
        self.assertEqual(res.status_code,200)

    #测试组件模块添加
    def test_module_add(self):
        system = T_SYSTEM(NAME="应用中心", DESCRIPTION="test", COMPANY="test",OWNER_ALL=True)
        system.save()
        res=self.client.post('/app_cmdb/module/add',{"NAME":"test","DESCRIPTION":"test","SYSTEM_ID":system.id,"OWNER":"onlyOne","RESPONSIBLE_PERSON":"1"})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

    #测试组件查询
    def test_module_select(self):
        res=self.client.get('/app_cmdb/module/select',{"limit":5,"offset":0,"order":"asc","ordername":"id","systemId":"0"})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

    #测试组件删除
    def test_module_delete(self):

        module=T_MODULE(NAME="test",DESCRIPTION="test",RESPONSIBLE_PERSON="1",OWNER_ALL=True)
        module.save()
        res=self.client.post('/app_cmdb/module/delete',{"id":module.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

    #测试组件修改
    def test_module_update(self):
        system = T_SYSTEM(NAME="应用中心", DESCRIPTION="test", COMPANY="test",OWNER_ALL=True)
        system.save()
        module=T_MODULE(NAME="test",DESCRIPTION="test",RESPONSIBLE_PERSON="1",OWNER_ALL=True)
        module.save()
        res=self.client.post('/app_cmdb/module/update',{"id":module.id,"NAME":"test1","DESCRIPTION":"test1","SYSTEM_ID":system.id,"OWNER":"onlyOne","RESPONSIBLE_PERSON":"1"})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

    #测试组件解绑
    def test_module_unwarp(self):
        system = T_SYSTEM(NAME="应用中心", DESCRIPTION="test", COMPANY="test",OWNER_ALL=True)
        system.save()
        module=T_MODULE(NAME="test",DESCRIPTION="test",RESPONSIBLE_PERSON="1",OWNER_ALL=True,SYSTEM_ID=system)
        module.save()
        res=self.client.post('/app_cmdb/module/unwarp',{"id":module.id,})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']


    def tearDown(self):
        print("moduledbTestCase======in tearDown")






class systemdbTestCase(TestCase):
    def setUp(self):
        print("systemdbTestCase======in setUp")
        # initClass=rolelist_permission()
        # initClass.init_role_user()
        role,created=RoleList.objects.get_or_create(name=u"超级管理员")
        role.save()
        user ,created= User.objects.get_or_create(username='jzyuan',mobile='15001994524', password=md5("88888888"),email='jiangchao_hubei@163.com',nickname='jzyuan',is_superuser="1",role=RoleList.objects.get(name=u"超级管理员"))
        user.save()
        res=self.client.post('/authority/user/login',{"USERNAME":"jzyuan","PASSWORD":"88888888"})
        print res.content
        self.assertEqual(res.status_code,200)

    #测试添加系统
    def test_system_add(self):
        res=self.client.post('/app_cmdb/system/add',{"NAME":"test","DESCRIPTION":"test","OWNER":"onlyOne","COMPANY":"1"})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

        #测试查询系统
    def test_system_select(self):
        res=self.client.get('/app_cmdb/system/select',{"offset":"1","limit":"5","order":"asc","ordername":"id","name":"","description":"","company":""})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

        #测试删除系统
    def test_system_delete(self):
        system = T_SYSTEM(NAME="应用中心", DESCRIPTION="test", COMPANY="test",OWNER_ALL=True)
        system.save()
        res=self.client.post('/app_cmdb/system/delete',{"id":system.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

        #测试修改系统
    def test_system_update(self):
        system = T_SYSTEM(NAME="应用中心", DESCRIPTION="test", COMPANY="test",OWNER_ALL=True)
        system.save()
        res=self.client.post('/app_cmdb/system/update',{"id":system.id,"NAME":"test","DESCRIPTION":"test1","OWNER":"onlyOne","COMPANY":"1"})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

        #     #测试系统导出xlsx
    # def test_system_export(self):
    #
    #     res=self.client.post('/app_cmdb/system/export',{"name":"","description":"","company":""})
    #     self.assertEqual(eval(res.content)['resultCode'],'0000')
    #     print eval(res.content)['resultDesc']
    #     return eval(res.content)['filepath']
    #
    # #测试系统xlsx下载
    # def test_system_download(self):
    #     filepath=self.test_system_export()
    #     res=self.client.get('/app_cmdb/system/export/download',{"filepath":filepath})
    #     print res.content


    def tearDown(self):
        print("systemdbTestCase======in tearDown")








class softwaredbTestCase(TestCase):
    def setUp(self):
        print("softwaredbTestCase======in setUp")
        # initClass=rolelist_permission()
        # initClass.init_role_user()
        role,created=RoleList.objects.get_or_create(name=u"超级管理员")
        role.save()
        user ,created= User.objects.get_or_create(username='jzyuan',mobile='15001994524', password=md5("88888888"),email='jiangchao_hubei@163.com',nickname='jzyuan',is_superuser="1",role=RoleList.objects.get(name=u"超级管理员"))
        user.save()
        res=self.client.post('/authority/user/login',{"USERNAME":"jzyuan","PASSWORD":"88888888"})
        print res.content
        self.assertEqual(res.status_code,200)

    #测试添加程序
    def test_software_add(self):
        system = T_SYSTEM(NAME="应用中心", DESCRIPTION="test", COMPANY="test",OWNER_ALL=True)
        system.save()
        module=T_MODULE(NAME="mysql",DESCRIPTION="test",RESPONSIBLE_PERSON="1",OWNER_ALL=True,SYSTEM_ID=system)
        module.save()
        res=self.client.post('/app_cmdb/software/add',{"NAME":"test","DESCRIPTION":"test","RESPONSIBLE_PERSON":"1","OWNER":"onlyOne","MODULE_ID":module.id,"LISTEN_PORT":"1",
                                                       "DEPLOY_DIR":"1","DEPLOY_ACCOUNT":"1","TIMER_SCRIPT":"1","LOG_EXPORT":"1","NOTE":"1","DATA_BACKUPPATH":"1","DATA_FILEPATH":"1"})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

        #测试查询程序
    def test_software_select(self):
        system = T_SYSTEM(NAME="应用中心", DESCRIPTION="test", COMPANY="test",OWNER_ALL=True)
        system.save()
        module=T_MODULE(NAME="mysql",DESCRIPTION="test",RESPONSIBLE_PERSON="1",OWNER_ALL=True,SYSTEM_ID=system)
        module.save()
        software=T_SOFTWARE(NAME="mysql",DESCRIPTION="test",RESPONSIBLE_PERSON="1",OWNER_ALL=True,MODULE_ID=module)
        software.save()
        res=self.client.get('/app_cmdb/software/select',{"offset":"1","limit":"5","order":"asc","ordername":"id","name":"","description":"","moduleId":module.id,"systemId":system.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        self.assertEqual(eval(res.content)['total'],1)
        print eval(res.content)['resultDesc']

        #测试删除程序
    def test_software_delete(self):
        software=T_SOFTWARE(NAME="mysql",DESCRIPTION="test",RESPONSIBLE_PERSON="1",OWNER_ALL=True)
        software.save()
        res=self.client.post('/app_cmdb/software/delete',{"id":software.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

        #测试修改程序
    def test_software_update(self):
        system = T_SYSTEM(NAME="应用中心", DESCRIPTION="test", COMPANY="test",OWNER_ALL=True)
        system.save()
        module=T_MODULE(NAME="mysql",DESCRIPTION="test",RESPONSIBLE_PERSON="1",OWNER_ALL=True,SYSTEM_ID=system)
        module.save()
        software=T_SOFTWARE(NAME="mysql",DESCRIPTION="test",RESPONSIBLE_PERSON="1",OWNER_ALL=True,MODULE_ID=module)
        software.save()
        res=self.client.post('/app_cmdb/software/update',{"id":software.id,"NAME":"test1","DESCRIPTION":"test1","RESPONSIBLE_PERSON":"11","OWNER":"onlyOne","MODULE_ID":module.id,"LISTEN_PORT":"11",
                                                       "DEPLOY_DIR":"11","DEPLOY_ACCOUNT":"11","TIMER_SCRIPT":"11","LOG_EXPORT":"11","NOTE":"11","DATA_BACKUPPATH":"11","DATA_FILEPATH":"1"})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

        #测试程序主机绑定
    def test_software_host_add(self):
        system = T_SYSTEM(NAME="应用中心", DESCRIPTION="test", COMPANY="test",OWNER_ALL=True)
        system.save()
        module=T_MODULE(NAME="mysql",DESCRIPTION="test",RESPONSIBLE_PERSON="1",OWNER_ALL=True,SYSTEM_ID=system)
        module.save()
        host=T_HOST(NAME="10.200.86.172",DESCRIPTION="test",VARIABLES="",MACHINE_TYPE="1",MACHINE_ROOM="1",SYSTEM_ID=system,
                    MACHINE_POSITION="1",CUTTER_NUMBER="1",SN_NUMBER="1",OS="1",PHYSICAL_MACHINE_TYPE="1",NOTE="1",OWNER_ALL=True)
        host.save()
        software=T_SOFTWARE(NAME="mysql",DESCRIPTION="test",RESPONSIBLE_PERSON="1",OWNER_ALL=True,MODULE_ID=module)
        software.save()
        res=self.client.post('/app_cmdb/software/host_add',{"id":software.id,"hostList":"[\""+host.NAME+"\"]"})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']
        return software.id,host.id

        #测试查询程序所拥有的所有主机
    def test_software_host_select(self):
        softwareId,hostId=self.test_software_host_add()
        res=self.client.get('/app_cmdb/software/host_select',{"offset":"1","limit":"5","order":"asc","ordername":"","id":softwareId})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        self.assertEqual(eval(res.content)['total'],1)
        print eval(res.content)['resultDesc']

        #测试解绑程序所拥有的主机
    def test_software_host_delete(self):
        softwareId,hostId=self.test_software_host_add()
        res=self.client.post('/app_cmdb/software/host_delete',{"id":hostId,"softwareId":softwareId})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']



    def tearDown(self):
        print("softwaredbTestCase======in tearDown")











class versiondbTestCase(TestCase):
    def setUp(self):
        print("versiondbTestCase======in setUp")
        # initClass=rolelist_permission()
        # initClass.init_role_user()
        role,created=RoleList.objects.get_or_create(name=u"超级管理员")
        role.save()
        user ,created= User.objects.get_or_create(username='jzyuan',mobile='15001994524', password=md5("88888888"),email='jiangchao_hubei@163.com',nickname='jzyuan',is_superuser="1",role=RoleList.objects.get(name=u"超级管理员"))
        user.save()
        res=self.client.post('/authority/user/login',{"USERNAME":"jzyuan","PASSWORD":"88888888"})
        print res.content
        self.assertEqual(res.status_code,200)

    #测试添加版本
    def test_version_add(self):
        system = T_SYSTEM(NAME="应用中心", DESCRIPTION="test", COMPANY="test",OWNER_ALL=True)
        system.save()
        module=T_MODULE(NAME="mysql",DESCRIPTION="test",RESPONSIBLE_PERSON="1",OWNER_ALL=True,SYSTEM_ID=system)
        module.save()
        software=T_SOFTWARE(NAME="mysql",DESCRIPTION="test",RESPONSIBLE_PERSON="1",OWNER_ALL=True,MODULE_ID=module)
        software.save()

        res=self.client.post('/app_cmdb/version/add',{"softwareId":software.id,"NAME":"1.0","DESCRIPTION":"test","INSTALL_PATH":"/opt"})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']
        return software.id

        #测试查询程序所拥有的所有版本
    def test_version_select(self):
        softwareId=self.test_version_add()
        res=self.client.get('/app_cmdb/version/select',{"offset":"1","limit":"5","order":"asc","ordername":"id","name":"","description":"","softwareId":softwareId})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        self.assertEqual(eval(res.content)['total'],1)
        print eval(res.content)['resultDesc']

        #测试解绑程序所拥有的主机
    def test_version_delete(self):
        system = T_SYSTEM(NAME="应用中心", DESCRIPTION="test", COMPANY="test",OWNER_ALL=True)
        system.save()
        module=T_MODULE(NAME="mysql",DESCRIPTION="test",RESPONSIBLE_PERSON="1",OWNER_ALL=True,SYSTEM_ID=system)
        module.save()
        software=T_SOFTWARE(NAME="mysql",DESCRIPTION="test",RESPONSIBLE_PERSON="1",OWNER_ALL=True,MODULE_ID=module)
        software.save()

        version = T_VERSION(NAME="1.2", DESCRIPTION="1",SOFTWARE_ID=software,INSTALL_PATH="1",PACKAGE_PATH="1",
                            OWNER_ALL=True
                            )
        version.save()
        res=self.client.post('/app_cmdb/version/delete',{"id":version.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print eval(res.content)['resultDesc']

    def tearDown(self):
        print("versiondbTestCase======in tearDown")