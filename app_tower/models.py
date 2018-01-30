# -*- coding: utf-8 -*
from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from djcelery import models as celery_models


# Create your models here.
#################################################################
#字段权限筛选
class checkOwnManager(models.Manager):
    def get_queryset(self):
        return super(checkOwnManager, self).get_queryset()
    #字段权限筛选方法,返回所有可用数据
    def check_own(self, request):
        print self.get_queryset()
        if request.session['isAdministrant']:
            return self.get_queryset()
        else:
            list=super(checkOwnManager, self).get_queryset()
            list1=list.filter(CREATE_USER_ID=request.session['userId']) | list.filter(CREATE_USER_ID=None)
            list2=list.filter(OWNER_ALL=True) | list1
            list3=list2 | list.filter(OWNER_PROJECT_ID__in=request.session['projectIdlist'])
            list4=list3 | list.filter(OWNER_ID=request.session['userId'])
            return list4
    #是否有该数据的使用权限
    def check_id(self,request,modelid):
        if request.session['isAdministrant']:
            return True
        else:
            try:
                model=self.model.objects.get(id=modelid)
            except Exception,e:
                print e
                return False
            if model.CREATE_USER_ID==request.session['userId'] or model.CREATE_USER_ID==None or model.OWNER_ALL or model.OWNER_PROJECT_ID in request.session['projectIdlist']:
                return True
            else:
                return False
    #是否有该数据的使用权限
    def check_name(self,request,name):
        if request.session['isAdministrant']:
            return True
        else:
            try:
                model=self.model.objects.get(NAME=name)
            except Exception,e:
                print e
                return False
            if model.CREATE_USER_ID==request.session['userId'] or model.CREATE_USER_ID==None or model.OWNER_ALL or model.OWNER_PROJECT_ID in request.session['projectIdlist']:
                return True
            else:
                return False
    def check_project(self, request, projectid):
        print self.get_queryset()
        if request.session['isAdministrant']:
            return self.get_queryset()
        else:
            list = super(checkOwnManager, self).get_queryset()
            list1 = list.filter(OWNER_PROJECT_ID=projectid)
            return list1
class T_PROJECT(models.Model):
    objects=checkOwnManager()
    NAME=models.CharField(max_length=128,unique=True)
    #描述
    DESCRIPTION=models.CharField(max_length=256,null=True,blank=True)
    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)
    #USERS=models.ManyToManyField(User,through='T_PROJECT_User_ID',through_fields=('PROJECT_ID','User_ID'))

    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #创建者
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #最后更新时间
    LAST_MODIFY_TIME=models.DateTimeField('修改时间',auto_now=True,null=True,blank=True)
    #最后更新者
    MODIFY_USER_ID=models.IntegerField(null=True,blank=True)



class T_HOST(models.Model):
    objects=checkOwnManager()
    #18	id,自增长
    #ID=models.AutoField(primary_key=True)
    #名字
    NAME=models.CharField(max_length=128)
    #描述
    DESCRIPTION=models.CharField(max_length=256)
    #变量
    VARIABLES=models.CharField(max_length=512)
     #1,0    =0不可用
    ENABLED=models.IntegerField(null=True,blank=True)
    #创建时间
    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
     #创建者
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #最后更新时间
    LAST_MODIFY_TIME=models.DateTimeField('修改时间',auto_now=True,null=True,blank=True)
    #最后更新者
    MODIFY_USER_ID=models.IntegerField(null=True,blank=True)
     #T_INVENTROY先用0
    INVENTORY_ID=models.IntegerField(default=0)
    #最后一个Jobid
    LAST_JOB_ID=models.IntegerField(null=True,blank=True)
    #是否有失败，暂时不用
    HAS_ACTIVE_FAILURES=models.BooleanField(default=True)
    #暂时不用
    HAS_EXTENRN_SOURCE=models.BooleanField(default=True)
    #使用者
    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)

    MACHINE_TYPE=models.CharField('机器类型',max_length=128,null=True,blank=True)
    MACHINE_ROOM=models.CharField('机房',max_length=128,null=True,blank=True)
    MACHINE_POSITION=models.CharField('机架位置',max_length=128,null=True,blank=True)
    CUTTER_NUMBER=models.CharField('刀框编号',max_length=128,null=True,blank=True)
    SN_NUMBER=models.CharField('SN号',max_length=128,null=True,blank=True)
    OS=models.CharField('os',max_length=128,null=True,blank=True)
    PHYSICAL_MACHINE_TYPE=models.CharField('物理机配置类型',max_length=128,null=True,blank=True)
    NOTE=models.CharField('备注',max_length=128,null=True,blank=True)
    SYSTEM_ID=models.ForeignKey('T_SYSTEM', null=True,blank=True,on_delete=models.PROTECT,related_name='SYSTEM_ID_T_HOST')
    ARGS1=models.CharField(max_length=128,null=True,blank=True)
    ARGS2=models.CharField(max_length=128,null=True,blank=True)
    ARGS3=models.CharField(max_length=128,null=True,blank=True)
    def natural_key(self):
        return (self.NAME,self.DESCRIPTION,self.MACHINE_TYPE,self.MACHINE_ROOM,self.MACHINE_POSITION,self.CUTTER_NUMBER,self.SN_NUMBER,self.OS,self.PHYSICAL_MACHINE_TYPE,self.NOTE,self.OWNER_ID,self.OWNER_NAME,self.OWNER_PROJECT_ID,self.OWNER_ALL,
                self.CREATE_TIME,self.CREATE_USER_ID,self.CREATE_USER_NAME,self.LAST_MODIFY_TIME,self.MODIFY_USER_ID) + self.SYSTEM_ID.natural_key()
    natural_key.dependencies = ['app_tower.T_SYSTEM']

class T_Group(models.Model):
    objects=checkOwnManager()
    #id,自增长
    #ID = models.AutoField(primary_key=True)
    #名字
    NAME=models.CharField(max_length=128,unique=True)
    #描述
    DESCRIPTION=models.CharField(max_length=256)
    #变量
    VARIABLES=models.CharField(max_length=512)
    #总体机器数
    TOTAL_HOSTS=models.IntegerField(null=True,blank=True)
    #创建时间
    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #创建者
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #最后更新时间
    LAST_MODIFY_TIME=models.DateTimeField('修改时间',auto_now=True,null=True,blank=True)
    #最后更新者
    MODIFY_USER_ID=models.IntegerField(null=True,blank=True)
    #T_INVENTROY先用0
    INVENTORY_ID=models.IntegerField(default=0)
    #暂时不用
    HAS_INVENTORY_SOURCE=models.BooleanField(default=True)
    #是否有失败，暂时不用
    HAS_ACTIVE_FAILURES=models.BooleanField(default=True)
    #暂时不用
    HAS_EXTENRN_SOURCE=models.BooleanField(default=True)
    #使用者
    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)
    #多对多关系
    HOSTS=models.ManyToManyField(T_HOST,through='T_GROUP_HOST_ID',through_fields=('GROUP_ID','HOST_ID'))

    def toJSON(self):
        import json
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))

class T_GROUP_HOST_ID(models.Model):
    #id,自增长
    #ID=models.AutoField(primary_key=True)
    #group id
    GROUP_ID=models.ForeignKey(T_Group, related_name='relations')
    # host id
    HOST_ID=models.ForeignKey(T_HOST, related_name='relations')

class playbook(models.Model):
    objects=checkOwnManager()
    #id,自增长
    #ID = models.AutoField(primary_key=True)
    #名字
    NAME=models.CharField(max_length=128,unique=True)
    #描述
    DESCRIPTION=models.CharField(max_length=256)
    FILEDIR=models.CharField(max_length=256,null=True,blank=True)
    #playbook文件路径
    PLAYBOOK_PATH=models.CharField(max_length=256)
    #playbook内容
    PLAYBOOK_CONTENT=models.TextField(null=True,blank=True)
    #创建时间
    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #创建者
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #最后更新时间
    LAST_MODIFY_TIME=models.DateTimeField('修改时间',auto_now=True,null=True,blank=True)
    #最后更新者
    MODIFY_USER_ID=models.IntegerField(null=True,blank=True)

    #使用者
    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)

    def natural_key(self):
        return (self.NAME)

class T_JOB_TEMPLATE(models.Model):
    objects=checkOwnManager()
    # id,自增长
    #ID = models.AutoField(primary_key=True)
    # 名字
    NAME = models.CharField(max_length=128,unique=True)
    # 描述
    DESCRIPTION = models.CharField(max_length=256)
    #Run/Check/Scan
    JOB_TYPE=models.CharField(max_length=32)
    #暂时不用支持1
    PROMPT_JOB_TYPE=models.IntegerField(null=True,blank=True)
    #T_GROUPID
    GROUP_ID=models.ForeignKey(T_Group,null=True,blank=True,on_delete=models.PROTECT,related_name='GROUP_ID_T_JOB_TEMPLATE')
    #T_PROJECT
    PROJECT_ID=models.IntegerField(null=True,blank=True)
    #T_PLAYBOOK
    PLAYBOOK_ID=models.ForeignKey(playbook,null=True,blank=True,on_delete=models.PROTECT,related_name='PLAYBOOK_ID_T_JOB_TEMPLATE')
    #PLAYBOOK文件名，暂时先用这个
    PLAYBOOK_FILE=models.CharField(max_length=256)
    #T_CREDENTIAL
    CREDENTIAL_MACHINE_ID=models.ForeignKey('T_LOGIN_CREDENTIALS',null=True,blank=True,on_delete=models.PROTECT,related_name='CREDENTIAL_MACHINE_ID_T_JOB_TEMPLATE')
    #并发数,0 表示默认,<=10
    FORKS=models.IntegerField(null=True,blank=True)
    #ansible的debug等级
    VERBOSITY=models.IntegerField(null=True,blank=True)
    #执行时参数
    JOB_TAGS=models.CharField(max_length=512)
    #执行时参数
    SKIP_TAGS=models.CharField(max_length=512)
    #使用过逗号分隔
    LABELS=models.CharField(max_length=128)
    #暂时不用支持
    PROMPT_JOB_TAGS=models.IntegerField(null=True,blank=True)
    #暂时不用支持
    PROMPT_SKIP_TAGS=models.IntegerField(null=True,blank=True)
    #暂时不用支持
    EXTRA_VARIABLES=models.CharField(max_length=512)
    #暂时不用支持
    PROMT_EXTRA_VAR=models.IntegerField(null=True,blank=True)
    #创建时间
    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #创建者
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #最后更新时间
    LAST_MODIFY_TIME=models.DateTimeField('修改时间',auto_now=True,null=True,blank=True)
    #最后更新者
    MODIFY_USER_ID=models.IntegerField(null=True,blank=True)
    ADMIN_ROLE_ID=models.IntegerField(null=True,blank=True)
    EXECUTE_ROLE_ID=models.IntegerField(null=True,blank=True)
    READ_ROLE_ID=models.IntegerField(null=True,blank=True)
    #INVENTORY
    INVENTORY_ID=models.IntegerField(null=True,blank=True)
    #使用者
    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)

    def natural_key(self):
        return (self.NAME,self.DESCRIPTION,self.JOB_TYPE,self.PLAYBOOK_FILE,self.CREATE_USER_NAME,self.CREATE_TIME,) + self.PLAYBOOK_ID.natural_key()
    natural_key.dependencies = ['app_tower.playbook']

class T_JOB(models.Model):
    objects=checkOwnManager()
    # id,自增长
    #ID = models.AutoField(primary_key=True)
    # 名字
    TEMPLETE_ID=models.ForeignKey(T_JOB_TEMPLATE,null=True,blank=True,on_delete=models.PROTECT,related_name='TEMPLETE_ID_T_JOB')
    NAME = models.CharField(max_length=128)
    # 描述
    DESCRIPTION = models.CharField(max_length=256)
    #Run/Check/Scan
    JOB_TYPE = models.CharField(max_length=32)
    #GROUPID
    GROUP_ID=models.ForeignKey(T_Group,null=True,blank=True,on_delete=models.PROTECT,related_name='GROUP_ID_T_JOB')
    #T_INVENTROY
    INVENTORY_ID=models.IntegerField(null=True,blank=True)
    #T_PROJECT
    PROJECT_ID=models.IntegerField(null=True,blank=True)
    #T_PLAYBOOK
    PLAYBOOK_ID=models.ForeignKey(playbook,null=True,blank=True,on_delete=models.PROTECT,related_name='PLAYBOOK_ID_T_JOB')
    #PLAYBOOK文件名，暂时先用这个
    PLAYBOOK_FILE=models.CharField(max_length=256)
    #T_CREDENTIAL
    CREDENTIAL_MACHINE_ID=models.ForeignKey('T_LOGIN_CREDENTIALS',null=True,blank=True,on_delete=models.PROTECT,related_name='CREDENTIAL_MACHINE_ID_T_JOB')
    #并发数,0 表示默认,<=10
    FORKS=models.IntegerField(null=True,blank=True)
    #ansible的debug等级
    VERBOSITY=models.IntegerField(null=True,blank=True)
    #执行时参数
    JOB_TAGS=models.CharField(max_length=512)
    #执行时参数
    SKIP_TAGS=models.CharField(max_length=512)
    #暂时不用支持
    EXTRA_VARIABLES=models.CharField(max_length=512)
    #以上参数从Jobtemplate处复制
    #创建时间
    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #创建者
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #开始时间
    START_TIME=models.DateTimeField(null=True,blank=True)
    #结束时间
    FINISH_TIME=models.DateTimeField(null=True,blank=True)
    #耗时，单位为耗时
    ELAPSED=models.IntegerField(null=True,blank=True)
    RESULT_STDOUT_TEXT=models.TextField(null=True,blank=True)
    #RESULT_STDOUT_FILE=
    #命令
    JOB_CWD=models.CharField(max_length=128)
    JOB_ENV=models.CharField(max_length=128)
    JOB_EXPLANATION=models.CharField(max_length=128)
    #执行参数
    JOB_ARGS=models.CharField(max_length=512)
    #执行Celery的taskid
    CELERY_TASK_ID=models.CharField(max_length=256)
    STATUS=models.CharField(max_length=32)
    #临时日志文件
    LOGFILE=models.CharField(max_length=256,null=True,blank=True)
    #日志内容入库
    LOGCONTENT=models.TextField(null=True,blank=True)
    #是否被取消了
    CANCEL_FLAG=models.BooleanField(default=False)
    #MANUAL/SCHEDULE
    LUNCH_TYPE=models.CharField(max_length=32)
    #使用者
    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)

class T_JOB_EVENT(models.Model):
    JOB_ID=models.IntegerField(null=True,blank=True)
    HOST_NAME=models.CharField(max_length=128)
    HOST_ID=models.IntegerField(null=True,blank=True)
    CREATE=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    MODIFY=models.DateTimeField('更新时间',auto_now=True,null=True,blank=True)

    SUCCESS=models.IntegerField(null=True,blank=True)
    FAILED=models.IntegerField(null=True,blank=True)
    CHANGED=models.IntegerField(null=True,blank=True)
    UNREACHABLE=models.IntegerField(null=True,blank=True)
    SKIPPED=models.IntegerField(null=True,blank=True)

class T_COMMAND_EVENT(models.Model):

    GROUP_ID=models.IntegerField(null=True,blank=True)
    CREDENTIALS_ID=models.IntegerField(null=True,blank=True)
    LOGFILE=models.CharField(max_length=64,null=True,blank=True)
    COMMAND_NAME=models.CharField(max_length=64,null=True,blank=True)
    COMMAND_VARS=models.CharField(max_length=128,null=True,blank=True)
    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)

    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    RESULT=models.TextField(null=True,blank=True)


class T_LOGIN_CREDENTIALS(models.Model):
    objects=checkOwnManager()
    #凭据名称
    NAME=models.CharField(max_length=64,unique=True)
    #描述
    DESCRIPTION=models.CharField(max_length=128)
    #使用者
    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)
    #类型
    TYPE=models.CharField(max_length=32)
    #登陆用户
    LOGIN_USER=models.CharField(max_length=32)
    #登录密码
    LOGIN_PWD=models.CharField(max_length=256)
    #特权名称
    PRIVILEGE_NAME=models.CharField(max_length=32,null=True,blank=True)
    #特权密码
    PRIVILEGE_PWD=models.CharField(max_length=256,null=True,blank=True)
    #创建者id
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    #创建者姓名
    CREATE_USER_NAME=models.CharField(max_length=64,null=True,blank=True)
    #创建时间
    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #最后修改人id
    LAST_MODIFY_USER_ID=models.IntegerField(null=True,blank=True)
    #最后修改时间
    LAST_MODIFY_TIME=models.DateTimeField('修改时间',auto_now=True,null=True,blank=True)

    def natural_key(self):
        return (self.NAME)

# 权限 表
class PermissionList(models.Model):
    name = models.CharField(max_length=64,unique=True)
    url = models.CharField(max_length=255,unique=True)

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.url)


class RoleList(models.Model):

    name = models.CharField(max_length=64,unique=True)
    permission =models.ManyToManyField(PermissionList,through='T_RoleList_PermissionList_ID',through_fields=('RoleList_ID','PermissionList_ID'))
    def natural_key(self):
        return (self.name)

    def __str__(self):
        return self.name



class T_RoleList_PermissionList_ID(models.Model):
    #id,自增长
    #ID=models.AutoField(primary_key=True)
    #group id
    RoleList_ID=models.ForeignKey(RoleList, related_name='relations')
    # host id
    PermissionList_ID=models.ForeignKey(PermissionList, related_name='relations')

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email,
                                username=username,
                                password=password,
                                )

        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True, db_index=True)
    mobile = models.CharField(max_length=512)
    createTime = models.DateTimeField('创建时间', auto_now_add=True, null=True, blank=True)
    gitLabToken=models.CharField(max_length=512,null=True, blank=True)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    nickname = models.CharField(max_length=64, null=True)
    sex = models.CharField(max_length=2, null=True)
    role = models.ForeignKey(RoleList, null=True, blank=True)
    projects=models.ManyToManyField(T_PROJECT,through='T_PROJECT_User_ID',through_fields=('User_ID','PROJECT_ID'))
    tools=models.ManyToManyField('T_TOOL',through='T_TOOL_User_ID',through_fields=('User_ID','TOOL_ID'))
    def natural_key(self):
        return (self.username,self.mobile,self.createTime,self.email,self.is_active,self.is_superuser,self.nickname,self.sex,) + self.role.natural_key()
    natural_key.dependencies = ['app_tower.RoleList']

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

class T_PROJECT_User_ID(models.Model):

    PROJECT_ID=models.ForeignKey(T_PROJECT, related_name='relations')
    # User id
    User_ID=models.ForeignKey(User, related_name='relations')
	
class JobStatusControl(models.Model):
    objects = checkOwnManager()
    # 时间
    TIME=models.DateTimeField('时间',null=True,blank=True)
    # 任务成功
    SUCCESS = models.IntegerField(null=True, blank=True,default=0)
    # 任务失败
    FAILURE = models.IntegerField(null=True, blank=True,default=0)
    # 任务取消
    REVOKED = models.IntegerField(null=True, blank=True,default=0)
    # 任务开始
    STARTED = models.IntegerField(null=True, blank=True,default=0)
    # 任务总数
    TOTAL_JOBS = models.IntegerField(null=True, blank=True,default=0)

    # 使用者
    OWNER_ID = models.IntegerField(null=True, blank=True)
    OWNER_NAME = models.CharField(max_length=128, null=True, blank=True)
    OWNER_PROJECT_ID = models.IntegerField(null=True, blank=True)
    OWNER_ALL = models.BooleanField(default=False)


class operation_record(models.Model):
    NAME=models.CharField(max_length=64,null=True,blank=True)
    PERMISSION_NAME=models.CharField(max_length=128,null=True,blank=True)
    URL=models.CharField(max_length=512,null=True,blank=True)
    REQUEST=models.CharField(max_length=1024,null=True,blank=True)
    REQUEST_BODY=models.TextField(null=True,blank=True)
    RESPONSE_CONTENT=models.TextField(null=True,blank=True)
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    #创建者姓名
    CREATE_USER_NAME=models.CharField(max_length=64,null=True,blank=True)
    #创建时间
    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #操作ip
    OPERATION_IP=models.CharField(max_length=64,null=True,blank=True)
    OPERATION_PORT=models.CharField(max_length=64,null=True,blank=True)
    #操作主机账户
    OPERATION_ACCOUNT=models.CharField(max_length=64,null=True,blank=True)
    #操作行为
    OPERATION_ACTION=models.CharField(max_length=128,null=True,blank=True)
    #操作说明
    OPERATION_DESCRIPTION=models.CharField(max_length=512,null=True,blank=True)

class sudo_record(models.Model):
    IP=models.CharField(max_length=64,null=True,blank=True)
    CREDENTIALS_ID=models.ForeignKey(T_LOGIN_CREDENTIALS, null=True, blank=True)
    ACCOUNT=models.CharField(max_length=64,null=True,blank=True)
    DESCRIPTION=models.CharField(max_length=512,null=True,blank=True)
    PORT=models.CharField(max_length=64,null=True,blank=True)
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    #创建者姓名
    CREATE_USER_NAME=models.CharField(max_length=64,null=True,blank=True)
    #创建时间
    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)

    def natural_key(self):
        return (self.IP,self.ACCOUNT,self.DESCRIPTION,self.PORT,self.CREATE_USER_ID,self.CREATE_USER_NAME,self.CREATE_TIME,) + self.CREDENTIALS_ID.natural_key()
    natural_key.dependencies = ['app_tower.T_LOGIN_CREDENTIALS']
#  意见反馈
class FEEDBACK(models.Model):
    # 意见主题
    TOPIC = models.CharField(max_length=64, null=True, blank=True)
    # 意见内容
    CONTENT = models.CharField(max_length=1024, null=True, blank=True)
    # 提意见姓名
    CREATE_USER_NAME = models.CharField(max_length=64, null=True, blank=True)
    # 创建时间
    CREATE_TIME = models.DateTimeField('创建时间', auto_now_add=True, null=True, blank=True)


PERIOD_CHOICES = (('days', ('Days')),
                  ('hours', ('Hours')),
                  ('minutes', ('Minutes')),
                  ('seconds', ('Seconds')),
                  ('microseconds', ('Microseconds')))
#  定时任务
class TimerTask(models.Model):
    objects=checkOwnManager()
    NAME=models.CharField(max_length=128,unique=True)
    DESCRIPTION = models.CharField(max_length=256,null=True, blank=True)
    JOBTEMPLETE_ID=models.ForeignKey(T_JOB_TEMPLATE,null=True,blank=True,on_delete=models.PROTECT,related_name='JOBTEMPLETE_ID_TimerTask')
    ISUSE=models.BooleanField(default=False)
    START_TIME=models.DateTimeField('开始时间', null=True, blank=True)
    EXPIRES_TIME=models.DateTimeField('过期时间', null=True, blank=True)
    EVERY=models.IntegerField(null=True,blank=True)
    PERIOD=models.CharField(max_length=24, null=True,blank=True)
    #celery task
    PERIODICTASK_ID=models.ForeignKey(celery_models.PeriodicTask,null=True,blank=True,related_name='PERIODICTASK_ID_TimerTask')
    #使用者
    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)

    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #创建者
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #最后更新时间
    LAST_MODIFY_TIME=models.DateTimeField('修改时间',auto_now=True,null=True,blank=True)
    #最后更新者
    MODIFY_USER_ID=models.IntegerField(null=True,blank=True)









#系统
class T_SYSTEM(models.Model):
    objects=checkOwnManager()
    NAME=models.CharField(max_length=128,unique=True)
    #责任公司
    COMPANY=models.CharField(max_length=64,null=True,blank=True)

    #描述
    DESCRIPTION=models.CharField(max_length=256,null=True,blank=True)
    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)

    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #创建者
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #最后更新时间
    LAST_MODIFY_TIME=models.DateTimeField('修改时间',auto_now=True,null=True,blank=True)
    #最后更新者
    MODIFY_USER_ID=models.IntegerField(null=True,blank=True)

    def natural_key(self):
        return (self.NAME)

#模块
class T_MODULE(models.Model):
    objects=checkOwnManager()
    NAME=models.CharField(max_length=128)
    #系统外键
    SYSTEM_ID=models.ForeignKey(T_SYSTEM, null=True,blank=True,on_delete=models.PROTECT,related_name='SYSTEM_ID_T_MODULE')
    #责任人
    RESPONSIBLE_PERSON=models.CharField(max_length=32,null=True,blank=True)
    #描述
    DESCRIPTION=models.CharField(max_length=256,null=True,blank=True)
    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)

    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #创建者
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #最后更新时间
    LAST_MODIFY_TIME=models.DateTimeField('修改时间',auto_now=True,null=True,blank=True)
    #最后更新者
    MODIFY_USER_ID=models.IntegerField(null=True,blank=True)

    def natural_key(self):
        return (self.NAME,self.DESCRIPTION,self.RESPONSIBLE_PERSON,self.OWNER_ID,self.OWNER_NAME,self.OWNER_PROJECT_ID,self.OWNER_ALL,
                self.CREATE_TIME,self.CREATE_USER_ID,self.CREATE_USER_NAME,self.LAST_MODIFY_TIME,self.MODIFY_USER_ID) + self.SYSTEM_ID.natural_key()
    natural_key.dependencies = ['app_tower.T_SYSTEM']

    def natural_software_key(self):
        return (self.NAME)

#程序
class T_SOFTWARE(models.Model):
    objects=checkOwnManager()
    NAME=models.CharField(max_length=128)
    #模块外键
    MODULE_ID=models.ForeignKey(T_MODULE, null=True,blank=True,on_delete=models.PROTECT,related_name='MODULE_ID_T_SOFTWARE')
    #ip(host)多对多外键
    HOSTS=models.ManyToManyField(T_HOST,through='T_SOFTWARE_HOST_ID',through_fields=('SOFTWARE_ID','HOST_ID'))
    #责任人
    RESPONSIBLE_PERSON=models.CharField(max_length=32,null=True,blank=True)
    #描述
    DESCRIPTION=models.CharField(max_length=256,null=True,blank=True)
    #默认监听端口
    LISTEN_PORT=models.IntegerField(null=True,blank=True)
    #默认部署目录
    DEPLOY_DIR=models.CharField(max_length=256,null=True,blank=True)
    #默认部署账号
    DEPLOY_ACCOUNT=models.CharField(max_length=32,null=True,blank=True)
    #定时脚本任务
    TIMER_SCRIPT=models.CharField(max_length=512,null=True,blank=True)
    #日志输出
    LOG_EXPORT=models.CharField(max_length=512,null=True,blank=True)
    #备注
    NOTE=models.CharField(max_length=512,null=True,blank=True)
    #数据备份路径
    DATA_BACKUPPATH=models.CharField(max_length=512,null=True,blank=True)
    #数据文件路径
    DATA_FILEPATH=models.CharField(max_length=512,null=True,blank=True)

    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)

    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #创建者
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #最后更新时间
    LAST_MODIFY_TIME=models.DateTimeField('修改时间',auto_now=True,null=True,blank=True)
    #最后更新者
    MODIFY_USER_ID=models.IntegerField(null=True,blank=True)

    ARGS1=models.CharField(max_length=128,null=True,blank=True)
    ARGS2=models.CharField(max_length=128,null=True,blank=True)
    ARGS3=models.CharField(max_length=128,null=True,blank=True)
    def natural_key(self):
        return (self.NAME,self.DESCRIPTION,self.RESPONSIBLE_PERSON,self.OWNER_ID,self.OWNER_NAME,self.OWNER_PROJECT_ID,self.OWNER_ALL,
                self.CREATE_TIME,self.CREATE_USER_ID,self.CREATE_USER_NAME,self.LAST_MODIFY_TIME,self.MODIFY_USER_ID,
                self.LISTEN_PORT,self.DEPLOY_DIR,self.DEPLOY_ACCOUNT,self.TIMER_SCRIPT,self.LOG_EXPORT,self.NOTE,self.DATA_BACKUPPATH,self.DATA_FILEPATH,
                ) + self.MODULE_ID.natural_software_key()
    natural_key.dependencies = ['app_tower.T_MODULE']


class T_SOFTWARE_HOST_ID(models.Model):
    #id,自增长
    #ID=models.AutoField(primary_key=True)
    #group id
    SOFTWARE_ID=models.ForeignKey(T_SOFTWARE, related_name='SOFTWARE_ID_T_SOFTWARE_HOST_ID')
    # host id
    HOST_ID=models.ForeignKey(T_HOST, related_name='HOST_ID_T_SOFTWARE_HOST_ID')
    #是否集群
    ISCOLONY=models.BooleanField(default=False)
    #集群虚地址
    LINEAR_ADDRESS=models.CharField(max_length=128,null=True,blank=True)
    #公网地址
    INTERNET_ADDRESS=models.CharField(max_length=128,null=True,blank=True)
    #域名
    DOMAIN_NAME=models.CharField(max_length=128,null=True,blank=True)
    #实际监听端口
    LISTEN_PORT=models.IntegerField(null=True,blank=True)
    #实际部署目录
    DEPLOY_DIR=models.CharField(max_length=256,null=True,blank=True)
    #实际部署账号
    DEPLOY_ACCOUNT=models.CharField(max_length=32,null=True,blank=True)

#包版本
class T_VERSION(models.Model):
    objects=checkOwnManager()
    #版本号
    NAME=models.FloatField(null=False,blank=False)
    # #版本号
    # VERSION_NUMBER=models.FloatField(null=True,blank=True)
    #描述
    DESCRIPTION=models.CharField(max_length=256,null=True,blank=True)
    #程序外键
    SOFTWARE_ID=models.ForeignKey(T_SOFTWARE, null=True,blank=True,on_delete=models.PROTECT,related_name='SOFTWARE_ID_T_VERSION')
    #默认安装路径
    INSTALL_PATH=models.CharField(max_length=256,null=True,blank=True)
    #软件包存储路径
    PACKAGE_PATH=models.CharField(max_length=256,null=True,blank=True)
    #默认应用
    ISUSE=models.BooleanField(default=True)

    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)

    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #创建者
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #最后更新时间
    LAST_MODIFY_TIME=models.DateTimeField('修改时间',auto_now=True,null=True,blank=True)
    #最后更新者
    MODIFY_USER_ID=models.IntegerField(null=True,blank=True)
    ARGS1=models.CharField(max_length=128,null=True,blank=True)
    ARGS2=models.CharField(max_length=128,null=True,blank=True)
    ARGS3=models.CharField(max_length=128,null=True,blank=True)



#工具
class T_TOOL(models.Model):
    objects=checkOwnManager()
    #工具名称
    NAME=models.CharField(max_length=128,unique=True)
    #说明
    DESCRIPTION=models.CharField(max_length=256,null=True,blank=True)
    #工具分类
    TOOLTYPE_ID=models.ForeignKey('T_TOOLTYPE', null=True,blank=True,on_delete=models.PROTECT,related_name='TOOLTYPE_ID_T_TOOL')
    #脚本语言
    SCRIPTLANGUAGE_CHIOCES = (
        (0, 'shell'),
        (1, 'python'),
        (2, 'yaml'),

    )
    SCRIPT_LANGUAGE=models.IntegerField(choices=SCRIPTLANGUAGE_CHIOCES,default=0)
    #脚本代码
    SCRIPT_CODE=models.TextField(null=True,blank=True)

    #审核状态
    AUDIT_CHIOCES = (
        (0, '未审核'),
        (1, '审核通过'),
        (2, '审核不通过'),

    )
    AUDIT_STATUS=models.IntegerField(choices=AUDIT_CHIOCES,default=0)
    #审核人
    AUDIT_USER_ID=models.IntegerField(null=True,blank=True)
    AUDIT_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #审核原因
    AUDIT_REASON=models.CharField(max_length=512,null=True,blank=True)
    AUDIT_TIME=models.DateTimeField('审核时间',null=True,blank=True)

    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)

    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #创建者
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #最后更新时间
    LAST_MODIFY_TIME=models.DateTimeField('修改时间',auto_now=True,null=True,blank=True)
    #最后更新者
    MODIFY_USER_ID=models.IntegerField(null=True,blank=True)
    ARGS1=models.CharField(max_length=128,null=True,blank=True)
    ARGS2=models.CharField(max_length=128,null=True,blank=True)
    ARGS3=models.CharField(max_length=128,null=True,blank=True)

class T_TOOL_User_ID(models.Model):

    TOOL_ID=models.ForeignKey(T_TOOL, related_name='TOOL_ID')
    # User id
    User_ID=models.ForeignKey(User, related_name='User_ID')
#工具分类
class T_TOOLTYPE(models.Model):
    objects=checkOwnManager()
    #分类名称
    NAME=models.CharField(max_length=128,unique=True)


#tool输入参数
class T_TOOL_INPUT(models.Model):
    objects=checkOwnManager()
    #参数名称
    NAME=models.CharField(max_length=128)
    #辅助说明
    DESCRIPTION=models.CharField(max_length=256,null=True,blank=True)
    #默认值
    DEFAULT=models.CharField(max_length=256,null=True,blank=True)
    #是否必填
    ISREQUIRED=models.BooleanField(default=False)
    #参数类型
    SCRIPTLANGUAGE_CHIOCES = (
        (0, '单行字符串'),
        (1, '多行字符串'),
        (2, '整型'),
        (3, '枚举'),
        (4, 'IP列表'),
        (5, 'JobTags'),
        (6, 'SkipTags'),
        (7, 'ExtraVariable'),
    )
    TYPE=models.IntegerField(choices=SCRIPTLANGUAGE_CHIOCES,default=0)
    #工具外键
    T_TOOL_ID=models.ForeignKey(T_TOOL, null=True,blank=True,related_name='T_TOOL_ID_T_TOOL_INPUT')

    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)

    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #创建者
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #最后更新时间
    LAST_MODIFY_TIME=models.DateTimeField('修改时间',auto_now=True,null=True,blank=True)
    #最后更新者
    MODIFY_USER_ID=models.IntegerField(null=True,blank=True)
    ARGS1=models.CharField(max_length=128,null=True,blank=True)
    ARGS2=models.CharField(max_length=128,null=True,blank=True)
    ARGS3=models.CharField(max_length=128,null=True,blank=True)


#tool输出参数
class T_TOOL_OUTPUT(models.Model):
    objects=checkOwnManager()
    #参数名称
    NAME=models.CharField(max_length=128)
    #辅助说明
    DESCRIPTION=models.CharField(max_length=256,null=True,blank=True)

    #参数类型
    SCRIPTLANGUAGE_CHIOCES = (
        (0, '字符串'),
        (1, '字典'),
        (2, '列表'),
        (3, '整型'),

    )
    TYPE=models.IntegerField(choices=SCRIPTLANGUAGE_CHIOCES,default=0)
    #工具外键
    T_TOOL_ID=models.ForeignKey(T_TOOL, null=True,blank=True,related_name='T_TOOL_ID_T_TOOL_OUTPUT')

    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)

    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #创建者
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #最后更新时间
    LAST_MODIFY_TIME=models.DateTimeField('修改时间',auto_now=True,null=True,blank=True)
    #最后更新者
    MODIFY_USER_ID=models.IntegerField(null=True,blank=True)
    ARGS1=models.CharField(max_length=128,null=True,blank=True)
    ARGS2=models.CharField(max_length=128,null=True,blank=True)
    ARGS3=models.CharField(max_length=128,null=True,blank=True)


class T_TOOL_EVENT(models.Model):
    objects=checkOwnManager()
    TOOL_ID=models.ForeignKey(T_TOOL, null=True,blank=True,related_name='TOOL_ID_T_TOOL_EVENT')
    CREDENTIALS_ID=models.ForeignKey(T_LOGIN_CREDENTIALS, null=True,blank=True,related_name='CREDENTIALS_ID_T_TOOL_EVENT')

    HOSTLIST=models.CharField(max_length=1024,null=True,blank=True)
    INPUTPARAMS=models.CharField(max_length=256,null=True,blank=True)

    #创建时间
    CREATE_TIME=models.DateTimeField('创建时间',auto_now_add=True,null=True,blank=True)
    #创建者
    CREATE_USER_ID=models.IntegerField(null=True,blank=True)
    CREATE_USER_NAME=models.CharField(max_length=128,null=True,blank=True)
    #开始时间
    START_TIME=models.DateTimeField(null=True,blank=True)
    #结束时间
    FINISH_TIME=models.DateTimeField(null=True,blank=True)
    #耗时，单位为耗时
    ELAPSED=models.IntegerField(null=True,blank=True)
    #执行Celery的taskid
    CELERY_TASK_ID=models.CharField(max_length=256)
    STATUS=models.CharField(max_length=32)
    #临时日志文件
    LOGFILE=models.CharField(max_length=256,null=True,blank=True)
    #日志内容入库
    LOGCONTENT=models.TextField(null=True,blank=True)
    #是否被取消了
    CANCEL_FLAG=models.BooleanField(default=False)
    #使用者
    OWNER_ID=models.IntegerField(null=True,blank=True)
    OWNER_NAME=models.CharField(max_length=128,null=True,blank=True)
    OWNER_PROJECT_ID=models.IntegerField(null=True,blank=True)
    OWNER_ALL=models.BooleanField(default=False)
    ARGS1=models.CharField(max_length=128,null=True,blank=True)
    ARGS2=models.CharField(max_length=128,null=True,blank=True)
    ARGS3=models.CharField(max_length=128,null=True,blank=True)







