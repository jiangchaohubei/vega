# /usr/bin/python2
# -*- coding:utf-8 -*-
from django.test import TestCase
from app_tower.models import User,RoleList,T_LOGIN_CREDENTIALS,T_Group,T_HOST,T_GROUP_HOST_ID,T_PROJECT,playbook,T_JOB_TEMPLATE,T_JOB
from authority.mysqldb.authoritydb import md5
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#登录凭证测试
class credentialsTestCase(TestCase):
    def setUp(self):
        print("credentialsTestCase======in setUp")

        role,created=RoleList.objects.get_or_create(name=u"超级管理员")
        role.save()
        user ,created= User.objects.get_or_create(username='jzyuan',mobile='15001994524', password=md5("88888888"),email='jiangchao_hubei@163.com',nickname='jzyuan',is_superuser="1",role=RoleList.objects.get(name=u"超级管理员"))
        user.save()
        res=self.client.post('/authority/user/login',{"USERNAME":"jzyuan","PASSWORD":"88888888"})

        self.assertEqual(res.status_code,200)

    #测试登录凭证添加
    def test_credentials_add(self):
        res=self.client.post('/app_tower/credentials/add',{"credentials_name":"test","credentials_desc":"test","credentials_owner":"onlyOne","credentials_type":"machine","credentials_loginUser":"root","credentials_password":"1qaz!QAZ",
                                                   "credentials_privilege":"su","privilege_password":"1qaz!QAZ"})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_credentials_add ',eval(res.content)['resultDesc']

    #测试登录凭证查询
    def test_credentials_select(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()
        res=self.client.get('/app_tower/credentials/select',{"limit":5,"offset":0,"order":"asc","ordername":"id","name":"","description":""})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        self.assertEqual(eval(res.content)['total'],1)
        print 'test_credentials_select ',eval(res.content)['resultDesc']

        #测试删除登录凭证
    def test_credentials_delete(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()
        res=self.client.post('/app_tower/credentials/delete',{"id":credentials.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_credentials_delete ',eval(res.content)['resultDesc']

        #测试登录凭证修改
    def test_credentials_update(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()
        res=self.client.post('/app_tower/credentials/update',{"id":credentials.id,"name":"test1","description":"test1","type":"machine","loginUser":"root","loginPassword":"2wsx@WSX","privilege":"su",
                                                           "privilegePassword":"2wsx@WSX","owner":"onlyOne"})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'credentials_update ',eval(res.content)['resultDesc']


    def tearDown(self):
        print("credentialsTestCase======in tearDown")










#主机组测试
class inventoriesdbTestCase(TestCase):
    def setUp(self):
        print("inventoriesdbTestCase======in setUp")

        role,created=RoleList.objects.get_or_create(name=u"超级管理员")
        role.save()
        user ,created= User.objects.get_or_create(username='jzyuan',mobile='15001994524', password=md5("88888888"),email='jiangchao_hubei@163.com',nickname='jzyuan',is_superuser="1",role=RoleList.objects.get(name=u"超级管理员"))
        user.save()
        res=self.client.post('/authority/user/login',{"USERNAME":"jzyuan","PASSWORD":"88888888"})

        self.assertEqual(res.status_code,200)

    #测试主机组添加
    def test_group_add(self):
        res=self.client.post('/app_tower/group/add',{"NAME":"test","DESCRIPTION":"test","group_owner":"onlyOne","VARIABLES":""})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_group_add ',eval(res.content)['resultDesc']

    #测试主机组查询
    def test_group_select(self):
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        res=self.client.get('/app_tower/group/select',{"limit":5,"offset":0,"order":"asc","ordername":"id","name":"","description":""})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        self.assertEqual(eval(res.content)['total'],1)
        print 'test_group_select ',eval(res.content)['resultDesc']

        #测试删除主机组
    def test_group_delete(self):
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        res=self.client.post('/app_tower/group/delete',{"id":group.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_group_delete ',eval(res.content)['resultDesc']

        #测试主机组修改
    def test_group_update(self):
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        res=self.client.post('/app_tower/group/update',{"id":group.id,"name":"test1","description":"test1","owner":"onlyOne","variables":""})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_group_update ',eval(res.content)['resultDesc']

    #     #测试主机组导出xlsx
    # def test_group_export(self):
    #
    #     res=self.client.post('/app_tower/group/export')
    #     self.assertEqual(eval(res.content)['resultCode'],'0000')
    #     self.assertEqual(res.status_code,200)
    #     print eval(res.content)['resultDesc']
    #     return eval(res.content)['filepath']

    # #测试主机组xlsx下载
    # def test_group_download(self):
    #     filepath=self.test_group_export()
    #     res=self.client.get('/app_tower/group/export/download',{"filepath":filepath})
    #     self.assertEqual(res.status_code,200)
    #     print res.content

        #测试主机组添加host
    def test_host_add(self):
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        host=T_HOST(NAME="10.200.86.172",DESCRIPTION="test",VARIABLES="",MACHINE_TYPE="1",MACHINE_ROOM="1",
                    MACHINE_POSITION="1",CUTTER_NUMBER="1",SN_NUMBER="1",OS="1",PHYSICAL_MACHINE_TYPE="1",NOTE="1",OWNER_ALL=True)
        host.save()
        res=self.client.post('/app_tower/host/add',{"id":group.id,"hostList":"[\""+host.NAME+"\"]"})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_host_add ',eval(res.content)['resultDesc']

    #测试查询主机组中host
    def test_host_select(self):
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        host=T_HOST(NAME="10.200.86.172",DESCRIPTION="test",VARIABLES="",MACHINE_TYPE="1",MACHINE_ROOM="1",
                    MACHINE_POSITION="1",CUTTER_NUMBER="1",SN_NUMBER="1",OS="1",PHYSICAL_MACHINE_TYPE="1",NOTE="1",OWNER_ALL=True)
        host.save()
        group_host,create = T_GROUP_HOST_ID.objects.get_or_create(GROUP_ID=group, HOST_ID=host)
        group_host.save()
        res=self.client.get('/app_tower/host/select',{"limit":5,"offset":0,"order":"asc","ordername":"id","id":group.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        self.assertEqual(eval(res.content)['total'],1)
        print 'test_host_select ',eval(res.content)['resultDesc']

        #测试删除主机组中主机
    def test_host_delete(self):
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        host=T_HOST(NAME="10.200.86.172",DESCRIPTION="test",VARIABLES="",MACHINE_TYPE="1",MACHINE_ROOM="1",
                    MACHINE_POSITION="1",CUTTER_NUMBER="1",SN_NUMBER="1",OS="1",PHYSICAL_MACHINE_TYPE="1",NOTE="1",OWNER_ALL=True)
        host.save()
        group_host,create = T_GROUP_HOST_ID.objects.get_or_create(GROUP_ID=group, HOST_ID=host)
        group_host.save()
        res=self.client.post('/app_tower/host/delete',{"id":host.id,"groupId":group.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_group_delete ',eval(res.content)['resultDesc']

    def tearDown(self):
        print("inventoriesdbTestCase======in tearDown")













#项目组测试
class projectTestCase(TestCase):
    def setUp(self):
        print("projectTestCase======in setUp")

        role,created=RoleList.objects.get_or_create(name=u"超级管理员")
        role.save()
        user ,created= User.objects.get_or_create(username='jzyuan',mobile='15001994524', password=md5("88888888"),email='jiangchao_hubei@163.com',nickname='jzyuan',is_superuser="1",role=RoleList.objects.get(name=u"超级管理员"))
        user.save()
        res=self.client.post('/authority/user/login',{"USERNAME":"jzyuan","PASSWORD":"88888888"})

        self.assertEqual(res.status_code,200)

    #测试项目组添加
    def test_project_add(self):
        res=self.client.post('/app_tower/project/add',{"NAME":"test","DESCRIPTION":"test","OWNER":"onlyOne","USERS":[]})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_project_add ',eval(res.content)['resultDesc']

    #测试项目组查询
    def test_project_select(self):
        project = T_PROJECT(NAME="test", DESCRIPTION="test",OWNER_ALL=True)
        project.save()
        res=self.client.get('/app_tower/project/select',{"limit":5,"offset":0,"order":"asc","ordername":"id","name":"","description":""})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        self.assertEqual(eval(res.content)['total'],1)
        print 'test_project_select ',eval(res.content)['resultDesc']

        #测试删除项目组
    def test_project_delete(self):
        project = T_PROJECT(NAME="test", DESCRIPTION="test",OWNER_ALL=True)
        project.save()
        res=self.client.post('/app_tower/project/delete',{"id":project.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_project_delete ',eval(res.content)['resultDesc']

        #测试项目组修改
    def test_project_update(self):
        project = T_PROJECT(NAME="test", DESCRIPTION="test",OWNER_ALL=True)
        project.save()
        res=self.client.post('/app_tower/project/update',{"id":project.id,"NAME":"test1","DESCRIPTION":"test1","OWNER":"onlyOne","USERS":[]})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_project_update ',eval(res.content)['resultDesc']


    def tearDown(self):
        print("projectTestCase======in tearDown")









#playbook测试
class playbookTestCase(TestCase):
    def setUp(self):
        print("playbookTestCase======in setUp")

        role,created=RoleList.objects.get_or_create(name=u"超级管理员")
        role.save()
        user ,created= User.objects.get_or_create(username='jzyuan',mobile='15001994524', password=md5("88888888"),email='jiangchao_hubei@163.com',nickname='jzyuan',is_superuser="1",role=RoleList.objects.get(name=u"超级管理员"))
        user.save()
        res=self.client.post('/authority/user/login',{"USERNAME":"jzyuan","PASSWORD":"88888888"})

        self.assertEqual(res.status_code,200)

    #测试playbook添加
    def test_playbook_add(self):
        res=self.client.post('/app_tower/playbook/add',{"name":"test","discription":"test","owner":"onlyOne","content":"test","dir":"","gitlabPath":"","gitProjectId":"","inputFile":""})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_playbook_add ',eval(res.content)['resultDesc']


    #测试playbook查询
    def test_playbook_select(self):
        pb = playbook(NAME="test", DESCRIPTION="test",PLAYBOOK_PATH="/opt/playbook/jzyuan/test.yaml", PLAYBOOK_CONTENT="test",OWNER_ALL=True,CREATE_USER_NAME="jzyuan",FILEDIR=None)
        pb.save()
        res=self.client.get('/app_tower/playbook/select',{"limit":5,"offset":0,"order":"asc","ordername":"id","name":"","userName":""})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        self.assertEqual(eval(res.content)['total'],1)
        print 'test_playbook_select ',eval(res.content)['resultDesc']

        #测试删除playbook
    def test_playbook_delete(self):
        pb = playbook(NAME="test", DESCRIPTION="test",PLAYBOOK_PATH="/opt/playbook/jzyuan/test.yaml", PLAYBOOK_CONTENT="test",OWNER_ALL=True,CREATE_USER_NAME="jzyuan",FILEDIR=None)
        pb.save()
        res=self.client.post('/app_tower/playbook/delete',{"id":pb.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_playbook_delete ',eval(res.content)['resultDesc']

        #测试playbook修改
    def test_playbook_update(self):
        pb = playbook(NAME="test", DESCRIPTION="test",PLAYBOOK_PATH="/opt/playbook/jzyuan/test.yaml", PLAYBOOK_CONTENT="test",OWNER_ALL=True,CREATE_USER_NAME="jzyuan",FILEDIR=None)
        pb.save()
        res=self.client.post('/app_tower/playbook/update',{"id":pb.id,"name":"test","description":"test","owner":"onlyOne","content":"test1","dir":""})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_playbook_update ',eval(res.content)['resultDesc']


    def tearDown(self):
        print("playbookTestCase======in tearDown")











#任务模板测试
class jobTemplatedbTestCase(TestCase):
    def setUp(self):
        print("jobTemplatedbTestCase======in setUp")

        role,created=RoleList.objects.get_or_create(name=u"超级管理员")
        role.save()
        user ,created= User.objects.get_or_create(username='jzyuan',mobile='15001994524', password=md5("88888888"),email='jiangchao_hubei@163.com',nickname='jzyuan',is_superuser="1",role=RoleList.objects.get(name=u"超级管理员"))
        user.save()
        res=self.client.post('/authority/user/login',{"USERNAME":"jzyuan","PASSWORD":"88888888"})

        self.assertEqual(res.status_code,200)

    #测试任务模板添加
    def test_job_add(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        pb = playbook(NAME="test", DESCRIPTION="test",PLAYBOOK_PATH="/opt/playbook/jzyuan/test.yaml", PLAYBOOK_CONTENT="test",OWNER_ALL=True,CREATE_USER_NAME="jzyuan",FILEDIR=None)
        pb.save()
        res=self.client.post('/app_tower/job/add',{"NAME":"test","DESCRIPTION":"test","JOB_TYPE":"Run","GROUP_ID":group.id,"PLAYBOOK_FILE":pb.id,"job_owner":"onlyOne","credentials":credentials.id,"FORKS":"1","JOB_TAGS":"","SKIP_TAGS":"","EXTRA_VARIABLES":"","LABELS":""})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_job_add ',eval(res.content)['resultDesc']


    #测试任务模板查询
    def test_job_select(self):
        self.test_job_add()
        res=self.client.get('/app_tower/job/select',{"limit":5,"offset":0,"order":"asc","ordername":"id","name":"","description":""})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        self.assertEqual(eval(res.content)['total'],1)
        print 'test_job_select ',eval(res.content)['resultDesc']

        #测试删除任务模板
    def test_job_delete(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        pb = playbook(NAME="test", DESCRIPTION="test",PLAYBOOK_PATH="/opt/playbook/jzyuan/test.yaml", PLAYBOOK_CONTENT="test",OWNER_ALL=True,CREATE_USER_NAME="jzyuan",FILEDIR=None)
        pb.save()
        job = T_JOB_TEMPLATE(NAME="test",DESCRIPTION="test",JOB_TYPE="Run",GROUP_ID=group,EXTRA_VARIABLES="",LABELS="",
                             PLAYBOOK_ID=pb,PLAYBOOK_FILE=pb.PLAYBOOK_PATH,CREDENTIAL_MACHINE_ID=credentials,  FORKS=4,JOB_TAGS="",SKIP_TAGS="",
                             OWNER_ALL=True)
        job.save()
        res=self.client.post('/app_tower/job/delete',{"id":job.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_job_delete ',eval(res.content)['resultDesc']

        #测试任务模板修改
    def test_job_update(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        pb = playbook(NAME="test", DESCRIPTION="test",PLAYBOOK_PATH="/opt/playbook/jzyuan/test.yaml", PLAYBOOK_CONTENT="test",OWNER_ALL=True,CREATE_USER_NAME="jzyuan",FILEDIR=None)
        pb.save()
        job = T_JOB_TEMPLATE(NAME="test",DESCRIPTION="test",JOB_TYPE="Run",GROUP_ID=group,EXTRA_VARIABLES="",LABELS="",
                             PLAYBOOK_ID=pb,PLAYBOOK_FILE=pb.PLAYBOOK_PATH,CREDENTIAL_MACHINE_ID=credentials,  FORKS=4,JOB_TAGS="",SKIP_TAGS="",
                             OWNER_ALL=True)
        job.save()
        res=self.client.post('/app_tower/job/update',{"id":job.id,"NAME":"test1","DESCRIPTION":"test1","JOB_TYPE":"Run","GROUP_ID":group.id,"PLAYBOOK_FILE":pb.id,"owner":"onlyOne","Login_credentials":credentials.id,"FORKS":"1","JOB_TAGS":"","SKIP_TAGS":"","EXTRA_VARIABLES":"","Labels":"test"})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_job_update ',eval(res.content)['resultDesc']

    def test_save_run_job(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        pb = playbook(NAME="test", DESCRIPTION="test",PLAYBOOK_PATH="/opt/playbook/jzyuan/test.yaml", PLAYBOOK_CONTENT="test",OWNER_ALL=True,CREATE_USER_NAME="jzyuan",FILEDIR=None)
        pb.save()
        res=self.client.post('/app_tower/job/save_run_job',{"NAME":"test","DESCRIPTION":"test","JOB_TYPE":"Run","GROUP_ID":group.id,"PLAYBOOK_FILE":pb.id,"job_owner":"onlyOne","credentials":credentials.id,"FORKS":"1","JOB_TAGS":"","SKIP_TAGS":"","EXTRA_VARIABLES":"","LABELS":""})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_save_run_job ',eval(res.content)['resultDesc']

    def test_run_job(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        pb = playbook(NAME="test", DESCRIPTION="test",PLAYBOOK_PATH="/opt/playbook/jzyuan/test.yaml", PLAYBOOK_CONTENT="test",OWNER_ALL=True,CREATE_USER_NAME="jzyuan",FILEDIR=None)
        pb.save()
        job = T_JOB_TEMPLATE(NAME="test",DESCRIPTION="test",JOB_TYPE="Run",GROUP_ID=group,EXTRA_VARIABLES="",LABELS="",
                             PLAYBOOK_ID=pb,PLAYBOOK_FILE=pb.PLAYBOOK_PATH,CREDENTIAL_MACHINE_ID=credentials,  FORKS=4,JOB_TAGS="",SKIP_TAGS="",
                             OWNER_ALL=True)
        job.save()
        res=self.client.post('/app_tower/job/run_job',{"id":job.id,"hostList":"[]","jobTags":"","skipTags":"","variable":""})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_run_job ',eval(res.content)['resultDesc']

    def test_run_commands_searchSN(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        res=self.client.post('/app_tower/job/run_commands_searchSN',{"groupid":group.id,"hostList":"[]","credentialsid":credentials.id})
        self.assertEqual(res.status_code,200)
        print 'test_run_commands_searchSN ',eval(res.content)

    def test_run_commands_searchLog(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        res=self.client.post('/app_tower/job/run_commands_searchLog',{"groupid":group.id,"hostList":"[]","credentialsid":credentials.id,"cmd":"grep","content":"","path":""})
        self.assertEqual(res.status_code,200)
        print 'test_run_commands_searchLog ',eval(res.content)

    def test_run_commands_copyFile(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        res=self.client.post('/app_tower/job/run_commands_copyFile',{"groupid":group.id,"hostList":"[]","credentialsid":credentials.id,"srcPath":"","desPath":""})
        self.assertEqual(res.status_code,200)
        print 'test_run_commands_copyFile ',eval(res.content)


    def test_run_commands_changeSudoAuth(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()

        res=self.client.post('/app_tower/job/run_commands_changeSudoAuth',{"hostList":"[]","credentialsid":credentials.id,"userName":"version","action":"search","port":"22","requestUser":"test"})
        self.assertEqual(res.status_code,200)
        print 'test_run_commands_changeSudoAuth ',eval(res.content)

    def test_run_commands_searchProcess(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()

        res=self.client.post('/app_tower/job/run_commands_searchProcess',{"hostList":"[]","credentialsid":credentials.id,"processName":"grep"})
        self.assertEqual(res.status_code,200)
        print 'test_run_commands_searchProcess ',eval(res.content)

    def test_run_commands_changeProcess(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()

        res=self.client.post('/app_tower/job/run_commands_changeProcess',{"hostList":"[]","credentialsid":credentials.id,"processName":"grep","operation":"stopped"})
        self.assertEqual(res.status_code,200)
        print 'test_run_commands_changeProcess ',eval(res.content)

    def test_run_commands_runSH(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        res=self.client.post('/app_tower/job/run_commands_runSH',{"groupid":group.id,"hostList":"[]","credentialsid":credentials.id,"vars":"cd /opt"})
        self.assertEqual(res.status_code,200)
        print 'test_run_commands_runSH ',eval(res.content)

    def test_review_file(self):
        pb = playbook(NAME="test", DESCRIPTION="test",PLAYBOOK_PATH="/opt/playbook/jzyuan/test.yaml", PLAYBOOK_CONTENT="test",OWNER_ALL=True,CREATE_USER_NAME="jzyuan",FILEDIR=None)
        pb.save()
        res=self.client.post('/app_tower/review_file',{"filePath":pb.id})
        self.assertEqual(res.status_code,200)
        print 'test_review_file ',eval(res.content)

        #测试sudo权限查询
    def test_sudo_select(self):

        res=self.client.get('/app_tower/job/sudo_select',{"limit":5,"offset":0,"order":"asc","ordername":"id","ip":"","account":"","createUser":""})
        self.assertEqual(res.status_code,200)
        self.assertEqual(eval(res.content)['total'],0)

    def test_sudoRecord_add(self):

        res=self.client.post('/app_tower/job/sudoRecord_add',{"addIP":"127.0.0.1","addPort":"22","addAccount":"root","addDesc":"test"})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_sudoRecord_add ',eval(res.content)['resultDesc']

        #测试操作记录查询
    def test_operation_select(self):

        res=self.client.get('/app_tower/job/operation_select',{"limit":5,"offset":0,"order":"asc","ordername":"id","name":"","createUser":""})
        self.assertEqual(res.status_code,200)

    def test_run_commands_change_passwd(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()

        res=self.client.post('/app_tower/job/run_commands_change_passwd',{"hostList":"[]","changepwd_credentials":credentials.id,"new_pwd":"Jc19931008?","user_name":"test"})
        self.assertEqual(res.status_code,200)
        print 'test_run_commands_change_passwd ',eval(res.content)

    def tearDown(self):
        print("jobTemplatedbTestCase======in tearDown")











#任务测试
class jobsdbTestCase(TestCase):
    def setUp(self):
        print("jobsdbTestCase======in setUp")

        role,created=RoleList.objects.get_or_create(name=u"超级管理员")
        role.save()
        user ,created= User.objects.get_or_create(username='jzyuan',mobile='15001994524', password=md5("88888888"),email='jiangchao_hubei@163.com',nickname='jzyuan',is_superuser="1",role=RoleList.objects.get(name=u"超级管理员"))
        user.save()
        res=self.client.post('/authority/user/login',{"USERNAME":"jzyuan","PASSWORD":"88888888"})

        self.assertEqual(res.status_code,200)

        #测试任务查询
    def test_jobs_select(self):
        res=self.client.get('/app_tower/jobs/select',{"limit":5,"offset":0,"order":"asc","ordername":"id","name":"","description":"","jobTaskid":"","jobType":"","jobStatus":""})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        self.assertEqual(eval(res.content)['total'],0)
        print 'test_jobs_select ',eval(res.content)['resultDesc']

        #测试删除任务记录
    def test_jobs_delete(self):
        credentials = T_LOGIN_CREDENTIALS(NAME="test",DESCRIPTION="test",OWNER_ALL=True,TYPE="machine",LOGIN_USER="test",LOGIN_PWD="1qaz!QAZ"
                                          ,PRIVILEGE_NAME="su",PRIVILEGE_PWD="1qaz!QAZ")
        credentials.save()
        group = T_Group(NAME="test", DESCRIPTION="test", VARIABLES="",OWNER_ALL=True)
        group.save()
        pb = playbook(NAME="test", DESCRIPTION="test",PLAYBOOK_PATH="/opt/playbook/jzyuan/test.yaml", PLAYBOOK_CONTENT="test",OWNER_ALL=True,CREATE_USER_NAME="jzyuan",FILEDIR=None)
        pb.save()
        job = T_JOB_TEMPLATE(NAME="test",DESCRIPTION="test",JOB_TYPE="Run",GROUP_ID=group,EXTRA_VARIABLES="",LABELS="",
                             PLAYBOOK_ID=pb,PLAYBOOK_FILE=pb.PLAYBOOK_PATH,CREDENTIAL_MACHINE_ID=credentials,  FORKS=4,JOB_TAGS="",SKIP_TAGS="",
                             OWNER_ALL=True)
        job.save()
        jobs = T_JOB(TEMPLETE_ID=job,NAME=job.NAME, DESCRIPTION=job.DESCRIPTION, JOB_TYPE=job.JOB_TYPE, GROUP_ID=job.GROUP_ID,
                     PROJECT_ID=job.PROJECT_ID, PLAYBOOK_ID=job.PLAYBOOK_ID,
                     PLAYBOOK_FILE=job.PLAYBOOK_FILE, CREDENTIAL_MACHINE_ID=job.CREDENTIAL_MACHINE_ID, FORKS=job.FORKS,
                     VERBOSITY=job.VERBOSITY, JOB_TAGS=job.JOB_TAGS,
                     SKIP_TAGS=job.SKIP_TAGS, EXTRA_VARIABLES=job.EXTRA_VARIABLES,
                     STATUS='STARTED',LOGFILE=file.name
                     ,OWNER_ID=job.OWNER_ID,OWNER_NAME=job.OWNER_NAME,OWNER_PROJECT_ID=job.OWNER_PROJECT_ID,OWNER_ALL=job.OWNER_ALL)
        jobs.save()
        res=self.client.post('/app_tower/jobs/delete',{"id":jobs.id})
        self.assertEqual(eval(res.content)['resultCode'],'0000')
        print 'test_jobs_delete ',eval(res.content)['resultDesc']

    def tearDown(self):
        print("jobsdbTestCase======in tearDown")

