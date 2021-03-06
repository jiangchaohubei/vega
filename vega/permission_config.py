# -*- coding:utf8 -*-


permissionList={
    'queryPermissionList':[
        {'name':'credentials_select','url':'/app_tower/credentials/select','cname':'查询登录凭证'},
        {'name':'group_select','url':'/app_tower/group/select','cname':'查询主机组'},
        {'name':'host_select','url':'/app_tower/host/select','cname':'查询主机组主机'},
        {'name':'jobTemplete_select','url':'/app_tower/job/select','cname':'查询任务模板'},
        {'name':'jobs_select','url':'/app_tower/jobs/select','cname':'查询任务'},
        {'name':'user_select','url':'/authority/select/user','cname':'查询用户'},
        {'name':'role_select','url':'/authority/select/role','cname':'查询角色'},
        {'name':'project_select','url':'/app_tower/project/select','cname':'查询项目组'},
        {'name':'playbook_select','url':'/app_tower/playbook/select','cname':'查询playbook'},
        {'name':'timerTask_select','url':'/app_tower/timerTask/select','cname':'查询定时任务'},
        {'name':'module_select','url':'/app_cmdb/module/select','cname':'查询模块'},
        {'name':'software_select','url':'/app_cmdb/software/select','cname':'查询程序'},
        {'name':'system_select','url':'/app_cmdb/system/select','cname':'查询系统'},
        {'name':'version_select','url':'/app_cmdb/version/select','cname':'查询版本'},
        {'name':'cmdb_host_select','url':'/app_cmdb/host/select','cname':'查询主机'},
        {'name':'history_select','url':'/app_tower/workingPlatform/history_select','cname':'查询作业执行历史'},
        {'name':'tool_select','url':'/app_tower/workingPlatform/tool_select','cname':'查询工具'},
    ],
    'workingPermissionList':[
        {'name':'tool_add','url':'/app_tower/workingPlatform/tool_add','cname':'新建工具'},
        {'name':'tool_update','url':'/app_tower/workingPlatform/tool_update','cname':'编辑工具'},
        {'name':'tool_delete','url':'/app_tower/workingPlatform/tool_delete','cname':'删除工具'},
        {'name':'tool_import','url':'/app_tower/workingPlatform/importTool','cname':'导入工具'},
        {'name':'tool_remove','url':'/app_tower/workingPlatform/removeTool','cname':'移除工具'},
        {'name':'tool_run','url':'/app_tower/workingPlatform/tool_run','cname':'执行工具'},
        {'name':'tool_audit','url':'/app_tower/workingPlatform/tool_audit','cname':'审核工具'},


    ],
    'hostPermissionList':[
        {'name':'cmdb_host_add','url':'/app_cmdb/host/add','cname':'添加主机'},
        {'name':'cmdb_host_delete','url':'/app_cmdb/host/delete','cname':'删除主机'},
        {'name':'cmdb_host_update','url':'/app_cmdb/host/update','cname':'修改主机'},
        {'name':'cmdb_host_export','url':'/app_cmdb/host/export','cname':'导出主机'},

    ],
    'versionPermissionList':[
        {'name':'version_add','url':'/app_cmdb/version/add','cname':'添加版本'},
        {'name':'version_delete','url':'/app_cmdb/version/delete','cname':'删除版本'},

    ],
    'softwarePermissionList':[
        {'name':'software_add','url':'/app_cmdb/software/add','cname':'添加程序'},
        {'name':'software_delete','url':'/app_cmdb/software/delete','cname':'删除程序'},
        {'name':'software_update','url':'/app_cmdb/software/update','cname':'修改程序'},
        {'name':'software_host_add','url':'/app_cmdb/software/host_add','cname':'绑定程序主机'},
        {'name':'software_host_select','url':'/app_cmdb/software/host_select','cname':'查询程序主机'},
        {'name':'software_host_delete','url':'/app_cmdb/software/host_delete','cname':'解绑程序主机'},

    ],
    'modulePermissionList':[
        {'name':'module_add','url':'/app_cmdb/module/add','cname':'添加模块'},
        {'name':'module_delete','url':'/app_cmdb/module/delete','cname':'删除模块'},
        {'name':'module_update','url':'/app_cmdb/module/update','cname':'修改模块'},

    ],
    'systemPermissionList':[
        {'name':'system_add','url':'/app_cmdb/system/add','cname':'添加系统'},
        {'name':'system_delete','url':'/app_cmdb/system/delete','cname':'删除系统'},
        {'name':'system_update','url':'/app_cmdb/system/update','cname':'修改系统'},
        {'name':'system_export','url':'/app_cmdb/system/export','cname':'导出系统'},
        {'name':'system_import','url':'/app_cmdb/system/import','cname':'导入系统'},

    ],
    'timerTaskPermissionList':[
        {'name':'timerTask_add','url':'/app_tower/timerTask/add','cname':'添加定时任务'},
        {'name':'timerTask_delete','url':'/app_tower/timerTask/delete','cname':'删除定时任务'},
        {'name':'timerTask_update','url':'/app_tower/timerTask/update','cname':'修改定时任务'},
        {'name':'timerTask_stop','url':'/app_tower/timerTask/stop','cname':'停止定时任务'},
        {'name':'timerTask_start','url':'/app_tower/timerTask/start','cname':'启用定时任务'},
    ],
    'playbookPermissionList':[
        {'name':'playbook_add','url':'/app_tower/playbook/add','cname':'添加playbook'},
        {'name':'playbook_delete','url':'/app_tower/playbook/delete','cname':'删除playbook'},
        {'name':'playbook_update','url':'/app_tower/playbook/update','cname':'修改playbook'},
    ],
    'credentialsPermissionList':[
        {'name':'credentials_add','url':'/app_tower/credentials/add','cname':'添加登录凭证'},
        {'name':'credentials_delete','url':'/app_tower/credentials/delete','cname':'删除登录凭证'},
        {'name':'credentials_update','url':'/app_tower/credentials/update','cname':'修改登录凭证'},
    ],
    'projectPermissionList':[
        {'name':'project_add','url':'/app_tower/project/add','cname':'添加项目组'},
        {'name':'project_delete','url':'/app_tower/project/delete','cname':'删除项目组'},
        {'name':'project_update','url':'/app_tower/project/update','cname':'修改项目组'},
    ],
    'groupPermissionList':[
        {'name':'group_add','url':'/app_tower/group/add','cname':'添加主机组'},
        {'name':'group_delete','url':'/app_tower/group/delete','cname':'删除主机组'},
        {'name':'group_update','url':'/app_tower/group/update','cname':'修改主机组'},
        {'name':'group_export','url':'/app_tower/group/export','cname':'导出主机组'},
        {'name':'group_add_backGroup','url':'/app_tower/group/create_backGroup','cname':'添加回滚主机组'},
        {'name':'host_add','url':'/app_tower/host/add','cname':'主机组添加主机'},
        {'name':'host_delete','url':'/app_tower/host/delete','cname':'主机组删除主机'},
        {'name':'host_update','url':'/app_tower/host/update','cname':'修改主机'},
    ],
    'jobTemplatePermissionList':[
        {'name':'jobTemplete_add','url':'/app_tower/job/add','cname':'添加任务模板'},
        {'name':'jobTemplete_run_save','url':'/app_tower/job/save_run_job','cname':'运行并添加任务模板'},
        {'name':'jobTemplete_run','url':'/app_tower/job/run_job','cname':'运行任务模板'},
        {'name':'jobTemplete_delete','url':'/app_tower/job/delete','cname':'删除任务模板'},
        {'name':'jobTemplete_update','url':'/app_tower/job/update','cname':'更新任务模板'},
    ],
    'jobPermissionList':[
        {'name':'jobs_delete','url':'/app_tower/jobs/delete','cname':'删除任务'},
        {'name':'jobs_stop','url':'/app_tower/job/stop_job','cname':'停止任务'},
    ],
    'userPermissionList':[
        {'name':'user_add','url':'/authority/save/user','cname':'添加用户'},
        {'name':'user_update','url':'/authority/update/user','cname':'修改用户'},
        {'name':'user_delete','url':'/authority/delete/user','cname':'删除用户'},
        {'name':'role_add','url':'/authority/add/role','cname':'添加角色'},
        {'name':'role_delete','url':'/authority/delete/role','cname':'删除角色'},
        {'name':'role_update','url':'/authority/update/role_permission','cname':'更新角色权限'},
    ],
    'feedbackPermissionList':[
        {'name':'saveFeedBack','url':'/feedback/saveFeedBack','cname':'添加意见反馈'},
        {'name':'exportAllFeedback','url':'/feedback/export/allFeedback','cname':'导出意见反馈'},
    ],
    'commandsPermissionList':[
        {'name':'change_passwd','url':'/app_tower/job/run_commands_change_passwd','cname':'修改用户密码'},
        {'name':'runSH','url':'/app_tower/job/run_commands_runSH','cname':'执行sh脚本'},
        {'name':'searchProcess','url':'/app_tower/job/run_commands_searchProcess','cname':'查询进程'},
        {'name':'changeProcess','url':'/app_tower/job/run_commands_changeProcess','cname':'启动/停止进程'},
        {'name':'updateSudo','url':'/app_tower/job/run_commands_changeSudoAuth','cname':'sudo权限操作'},
        {'name':'callbackSudo','url':'/app_tower/job/run_commands_callbackSudoAuth','cname':'回收sudo权限'},
        {'name':'searchLog','url':'/app_tower/job/run_commands_searchLog','cname':'查日志'},
        {'name':'copyFile','url':'/app_tower/job/run_commands_copyFile','cname':'分发文件'},
        {'name':'searchSN','url':'/app_tower/job/run_commands_searchSN','cname':'查询SN号'},

    ],
    'datastatisticsPermissionList':[
        {'name':'sudo_add','url':'/app_tower/job/sudoRecord_add','cname':'添加sudo权限记录'},
        {'name':'sudo_delete','url':'/app_tower/job/sudo_delete','cname':'删除sudo权限记录'},
        {'name':'sudo_select','url':'/app_tower/job/sudo_select','cname':'sudo权限统计'},
        {'name':'operation_select','url':'/app_tower/job/operation_select','cname':'操作记录统计'},
        {'name':'JobStatus_select','url':'/authority/charts/JobStatusStatics/JobStatus','cname':'任务状态统计'},



    ]
}


roleList=[
    {
        'name':'超级管理员',
        'permissionList':[
            'credentials_select','group_select','host_select','jobTemplete_select','jobs_select','user_select','role_select','project_select','playbook_select','timerTask_select','module_select','software_select','system_select','version_select','cmdb_host_select','history_select','tool_select',
            'credentials_add','credentials_delete','credentials_update',
            'playbook_add','playbook_delete','playbook_update',
            'project_add','project_delete','project_update',
            'group_add', 'group_delete','group_update','group_export','group_add_backGroup','host_add','host_delete','host_update',
            'jobTemplete_add', 'jobTemplete_run_save','jobTemplete_run','jobTemplete_delete','jobTemplete_update',
            'jobs_delete', 'jobs_stop',
            'user_add','user_update','user_delete', 'role_add','role_delete','role_update',
            'saveFeedBack','exportAllFeedback',
            'updateSudo','searchLog','copyFile','searchSN','changeProcess','searchProcess','runSH','callbackSudo','change_passwd',
            'sudo_select','operation_select','JobStatus_select','sudo_add','sudo_delete',
            'timerTask_add','timerTask_delete','timerTask_update','timerTask_stop','timerTask_start',

            'cmdb_host_add','cmdb_host_delete','cmdb_host_update','cmdb_host_export',
            'version_add','version_delete',
            'software_add','software_delete','software_update','software_host_add','software_host_delete','software_host_select',
            'module_add','module_delete','module_update',
            'system_add','system_delete','system_update','system_export','system_import',

            'tool_add','tool_update','tool_delete','tool_import','tool_remove','tool_run','tool_audit',

        ]
    },
    {
        'name':'管理员',
        'permissionList': [
            'credentials_select','group_select','host_select','jobTemplete_select','jobs_select','user_select','role_select','project_select','playbook_select','timerTask_select','module_select','software_select','system_select','version_select','cmdb_host_select','history_select','tool_select',
            'credentials_add','credentials_delete','credentials_update',
            'playbook_add','playbook_delete','playbook_update',
            'project_add','project_delete','project_update',
            'group_add', 'group_delete','group_update','group_export','group_add_backGroup','host_add','host_delete','host_update',
            'jobTemplete_add', 'jobTemplete_run_save','jobTemplete_run','jobTemplete_delete','jobTemplete_update',
            'jobs_delete', 'jobs_stop',
            'user_add','user_update','user_delete', 'role_add','role_delete','role_update',
            'saveFeedBack','exportAllFeedback',
            'updateSudo','searchLog','copyFile','searchSN','changeProcess','searchProcess','runSH','callbackSudo','change_passwd',
            'sudo_select','operation_select','JobStatus_select','sudo_add','sudo_delete',
            'timerTask_add','timerTask_delete','timerTask_update','timerTask_stop','timerTask_start',

            'cmdb_host_add','cmdb_host_delete','cmdb_host_update','cmdb_host_export',
            'version_add','version_delete',
            'software_add','software_delete','software_update','software_host_add','software_host_delete','software_host_select',
            'module_add','module_delete','module_update',
            'system_add','system_delete','system_update','system_export','system_import',

            'tool_add','tool_update','tool_delete','tool_import','tool_remove','tool_run','tool_audit',
        ]
    },
    {
        'name':'运维人员',
        'permissionList': [
            'credentials_select','group_select','host_select','jobTemplete_select','jobs_select','project_select','playbook_select','timerTask_select','module_select','software_select','system_select','version_select','cmdb_host_select','history_select','tool_select',
            'credentials_add','credentials_delete','credentials_update',
            'playbook_add','playbook_delete','playbook_update',
            'project_add','project_delete','project_update',
            'group_add', 'group_delete','group_update','group_export','group_add_backGroup','host_add','host_delete','host_update',
            'jobTemplete_add', 'jobTemplete_run_save','jobTemplete_run','jobTemplete_delete','jobTemplete_update',
            'jobs_delete', 'jobs_stop',
            'saveFeedBack','exportAllFeedback',
            'updateSudo','searchLog','copyFile','searchSN','changeProcess','searchProcess','runSH','callbackSudo','change_passwd',
            'sudo_select','operation_select','JobStatus_select','sudo_add','sudo_delete',
            'timerTask_add','timerTask_delete','timerTask_update','timerTask_stop','timerTask_start',

            'cmdb_host_add','cmdb_host_delete','cmdb_host_update','cmdb_host_export',
            'version_add','version_delete',
            'software_add','software_delete','software_update','software_host_add','software_host_delete','software_host_select',
            'module_add','module_delete','module_update',
            'system_add','system_delete','system_update','system_export','system_import',

            'tool_add','tool_update','tool_delete','tool_import','tool_remove','tool_run',

        ]
    },
    {
        'name':'游客',
        'permissionList': [
            'credentials_select','group_select','host_select','jobTemplete_select','jobs_select','user_select','role_select','project_select','playbook_select','timerTask_select','module_select','software_select','system_select','version_select','cmdb_host_select','history_select','tool_select',
        ]
    },

]



