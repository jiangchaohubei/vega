# -*- coding: utf-8 -*
from django.test import TestCase
from mysqldb import authoritydb
from app_tower.models import User,RoleList,PermissionList,T_RoleList_PermissionList_ID
from vega.rolelist_permissionlist_init import rolelist_permission
from authority.mysqldb.authoritydb import md5
# Create your tests here.

class authoritydbTestCase(TestCase):
    def setUp(self):
        print("authoritydbTestCase======in setUp")
        # initClass=rolelist_permission()
        # initClass.init_role_user()
        role,created=RoleList.objects.get_or_create(name=u"超级管理员")
        role.save()
        user ,created= User.objects.get_or_create(username='jzyuan',mobile='15001994524', password=md5("88888888"),email='jiangchao_hubei@163.com',nickname='jzyuan',is_superuser="1",role=RoleList.objects.get(name=u"超级管理员"))
        user.save()

    #生成手机验证码
    def test_createPhoneCode(self):
        verifyCode=authoritydb.createPhoneCode()
        print verifyCode
        self.assertRegexpMatches(verifyCode,'[0-9]{6}')

    # #获取验证码
    # def test_loginCapcha_success(self):
    #     res=self.client.post('/authority/user/loginCapcha',{"userName":"jzyuan","password":"88888888"})
    #     self.assertEqual(res.status_code,200)

    #登录
    def test_login(self):
        res=self.client.post('/authority/user/loginCapcha',{"userName":"jzyuan","password":"88888888"})
        self.assertEqual(res.status_code,200)
        res=self.client.post('/authority/user/login',{"USERNAME":"jzyuan","PASSWORD":"88888888"})
        print res.content
        self.assertEqual(res.status_code,200)

    #注销
    def test_logout(self):
        res=self.client.post('/authority/user/logout')
        self.assertEqual(res.status_code,200)

    #  #测试用户是否已经注册
    def test_checkUserName(self):
        res=self.client.post('/authority/user/checkUserName',{'userName':'jzyuan'})
        print res.content
        self.assertEqual(res.content,'false') #已经注册
        res=self.client.post('/authority/user/checkUserName',{'userName':'11111'})
        print res.content
        self.assertEqual(res.content,'true') #已经注册

        #测试用户是否存在
    def test_checkUserQuestion(self):
        res=self.client.post('/authority/user/checkUserQuestion',{'userName':'jzyuan'})
        print res.content
        self.assertEqual(eval(res.content)['result'],'Success!')
        res=self.client.post('/authority/user/checkUserQuestion',{'userName':'11111'})
        print res.content
        self.assertEqual(eval(res.content)['result'],'FAIELD!')

    #     #测试根据邮箱重置密码
    # def test_resetPasswordByEmail(self):
    #     res=self.client.post('/authority/user/reset/password/email',{'userName':'jzyuan','email':'jiangchao_hubei@163.com'})
    #     print res.content
    #     self.assertEqual(eval(res.content)['result'],'Success!')

    #     #测试根据手机号重置密码
    # def test_resetPasswordByMobile(self):
    #     res=self.client.post('/authority/user/reset/password/mobile',{'userName':'jzyuan','mobile':'15001994524'})
    #     print res.content
    #     self.assertEqual(res.status_code,200)

    #测试用户修改密码
    def test_updatepassword(self):
        self.test_login()
        res=self.client.post('/authority/user/updatepassword',{"oldPassword":"88888888","newPassword":"216612","new_repassword":"216612"})
        print res.content
        self.assertEqual(eval(res.content)['result'],"Success!")

    #测试发送短信验证码
#     def test_getResponseData(self):
#         Usermobile='15001994524'
#         content="【咪咕视讯】，动态密码：" + '666666' + "（切勿告诉他人）,该验证码用于自动化部署系统登陆,5分钟有效"
#         url = 'http://172.16.9.132/mtv/HttpSendSM?userName=ZDHBS&password=1qaz!QAZ&srcId=1065802710111&channel=1&destMsisdn='+Usermobile+'&content='+content+'&needReport=1'
#         str=authoritydb.getResponseData(url)
#         print str

    #测试查询用户
    def test_selectUser(self):
        self.test_login()
        res=self.client.get('/authority/select/user',{"limit":5,"offset":0,"order":"asc","username":"jzyuan","mobile":"","nickname":"jz","email":""})

        self.assertEqual(eval(res.content)['result'],"Success")

        #测试查询角色
    def test_selectRole(self):
        self.test_login()
        res=self.client.get('/authority/select/role',{"limit":5,"offset":0,"order":"asc","ordername":"id","name":"运维人员"})

        self.assertEqual(eval(res.content)['result'],"Success")

        #测试删除用户
    def test_delete(self):
        role,created=RoleList.objects.get_or_create(name=u"运维人员")
        role.save()
        user ,created= User.objects.get_or_create(username='yunwei',mobile='15001994524', password=md5("88888888"),email='jiangchao_hubei@163.com',nickname='jzyuan',role=RoleList.objects.get(name=u"运维人员"))
        user.save()
        self.test_login()
        res1=self.client.post('/authority/delete/user',{"id":user.id,"username":user.username})
        self.assertEqual(eval(res1.content)['result'],"Success")
        res2=self.client.post('/authority/delete/user',{"id":1,"username":"Admin"})
        self.assertEqual(eval(res2.content)['result'],"FAIELD!")

    #测试添加用户
    def test_saveUser(self):
        self.test_login()
        res=self.client.post('/authority/save/user',{"username":"testUser","mobile":"15001994524","email":"jiangchao_hubei@163.com","nickname":"jc","role":u"超级管理员",})
        self.assertEqual(eval(res.content)['result'],"Success!")

    #测试修改用户
    def test_updateUser(self):
        self.test_login()
        role,created=RoleList.objects.get_or_create(name=u"运维人员")
        role.save()
        user ,created= User.objects.get_or_create(username='yunwei',mobile='15001994524', password=md5("88888888"),email='jiangchao_hubei@163.com',nickname='jzyuan',role=RoleList.objects.get(name=u"运维人员"))
        user.save()
        res=self.client.post('/authority/update/user',{"id":user.id,"username":"updateUser","mobile":"15671624674","email":"jiangchao_hubei@126.com","nickname":"jc","role":u"超级管理员",})
        self.assertEqual(eval(res.content)['resultCode'],"0000")
        self.assertEqual(User.objects.get(id=user.id).username,"updateUser")
        self.assertEqual(User.objects.get(id=user.id).mobile,"15671624674")
        self.assertEqual(User.objects.get(id=user.id).email,"jiangchao_hubei@126.com")

        #测试添加角色
    def test_addRole(self):
        self.test_login()
        res=self.client.post('/authority/add/role',{"roleName":"test"})
        self.assertEqual(eval(res.content)['result'],"Success!")

        #测试删除角色
    def test_deleteRole(self):
        self.test_login()
        role,created=RoleList.objects.get_or_create(name=u"运维人员")
        role.save()
        res=self.client.post('/authority/delete/role',{"roleName":u"运维人员"})
        self.assertEqual(eval(res.content)['result'],"Success!")

    #     #测试获取权限列表
    # def test_select_parentPermission(self):
    #     initClass=rolelist_permission()
    #     initClass.init_role_user()
    #     self.test_login()
    #
    #     res=self.client.post('/authority/select/parentPermission',{"title":u"查询","id":"1"})
    #     print res.content
    #     self.assertEqual(eval(res.content)['result'],"Success!")


    def tearDown(self):
        print("authoritydbTestCase======in tearDown")
