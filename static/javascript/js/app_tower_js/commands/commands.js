/**
 * Created by PC on 2017/8/15.
 */
var SN_hosts=[]
var LOG_hosts=[]
var CopyFile_hosts=[]
var RunSH_hosts=[]
var changeAuth_hosts=[]
var searchProcess_hosts=[]
var changeProcess_hosts=[]
var changepwd_hosts=[]
$(function () {
    //textarea全屏
    $('#log').textareafullscreen();
    $("#group").html("");
    $("#searchLog_group").html("");
    $("#copy_group").html("");
    $("#searchSN_group").html("");
    $("#runSH_group").html("");
    $("#changeAuth_group").html("");
    $("#searchProcess_group").html("");
    $("#changeProcess_group").html("");
    $("#group").append("<option value='0' selected>空组</option>");
    $("#searchLog_group").append("<option value='0' selected>空组</option>");
    $("#copy_group").append("<option value='0' selected>空组</option>");
    $("#searchSN_group").append("<option value='0' selected>空组</option>");
    $("#runSH_group").append("<option value='0' selected>空组</option>");
    $("#changeAuth_group").append("<option value='0' selected>空组</option>");
    $("#searchProcess_group").append("<option value='0' selected>空组</option>");
    $("#changeProcess_group").append("<option value='0' selected>空组</option>");
    $.ajax({
        type: 'POST',
        url: "/app_tower/job/init_commands_select",
        data: {},
        dataType: "json",
        success: function (data) {
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            for (var i = 0; i < data.groupList.length; i++) {
                $("#group").append("<option value='" + data.groupList[i].pk + "'>" + data.groupList[i].fields.NAME + "</option>");
                $("#searchLog_group").append("<option value='" + data.groupList[i].pk + "'>" + data.groupList[i].fields.NAME + "</option>");
                $("#copy_group").append("<option value='" + data.groupList[i].pk + "'>" + data.groupList[i].fields.NAME + "</option>");
                $("#searchSN_group").append("<option value='" + data.groupList[i].pk + "'>" + data.groupList[i].fields.NAME + "</option>");
                $("#runSH_group").append("<option value='" + data.groupList[i].pk + "'>" + data.groupList[i].fields.NAME + "</option>");
                $("#changeAuth_group").append("<option value='" + data.groupList[i].pk + "'>" + data.groupList[i].fields.NAME + "</option>");
                $("#searchProcess_group").append("<option value='" + data.groupList[i].pk + "'>" + data.groupList[i].fields.NAME + "</option>");
                $("#changeProcess_group").append("<option value='" + data.groupList[i].pk + "'>" + data.groupList[i].fields.NAME + "</option>");
                $("#changepwd_group").append("<option value='" + data.groupList[i].pk + "'>" + data.groupList[i].fields.NAME + "</option>");
            }
            for (var i = 0; i < data.credentialsList.length; i++) {
                $("#credentials").append("<option value='" + data.credentialsList[i].pk + "'>" + data.credentialsList[i].fields.NAME + "</option>");
                $("#searchLog_credentials").append("<option value='" + data.credentialsList[i].pk + "'>" + data.credentialsList[i].fields.NAME + "</option>");
                $("#copy_credentials").append("<option value='" + data.credentialsList[i].pk + "'>" + data.credentialsList[i].fields.NAME + "</option>");
                $("#searchSN_credentials").append("<option value='" + data.credentialsList[i].pk + "'>" + data.credentialsList[i].fields.NAME + "</option>");
                $("#auth_credentials").append("<option value='" + data.credentialsList[i].pk + "'>" + data.credentialsList[i].fields.NAME + "</option>");
                $("#searchProcess_credentials").append("<option value='" + data.credentialsList[i].pk + "'>" + data.credentialsList[i].fields.NAME + "</option>");
                $("#changeProcess_credentials").append("<option value='" + data.credentialsList[i].pk + "'>" + data.credentialsList[i].fields.NAME + "</option>");
                $("#runSH_credentials").append("<option value='" + data.credentialsList[i].pk + "'>" + data.credentialsList[i].fields.NAME + "</option>");
                $("#changepwd_credentials").append("<option value='" + data.credentialsList[i].pk + "'>" + data.credentialsList[i].fields.NAME + "</option>");
            }

            onSNGroupChange();
            onLOGGroupChange();
            onCOPYGroupChange();
            onRunSHGroupChange();

            onGroupChange('changeAuth_group','authIp','writeAUTHHost','chooseAUTHHost',changeAuth_hosts);
            onGroupChange('searchProcess_group','searchProcessIp','writeSearchProcessHost','chooseSearchProcessHost',searchProcess_hosts);
            onGroupChange('changeProcess_group','changeProcessIp','writeChangeProcessHost','chooseChangeProcessHost',changeProcess_hosts);
            onGroupChange('changepwd_group','changepwdIp','writeChangepwdHost','chooseChangepwdHost',changepwd_hosts);

        },
        error: function () {
            console.log("error");
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })

})

function onGroupChange(groupDivId,divId,inputId,selectId,hosts) {
    $("#"+selectId).html('')
    if ($('#'+groupDivId).val()=='0'){
        $('#'+divId).html("");
        $('#'+divId).append('<input type="text" class="form-control" placeholder="请输入ip"  id="'+inputId+'"  style="display: block">')
        hosts.splice(0,hosts.length)
        $('#'+inputId).bind('input propertychange', function () {
            hosts.splice(0,hosts.length)
            hosts.push($(this).val())
        })
        return;
    }else{
        $('#'+divId).html("");
        $('#'+divId).append('<select id="'+selectId+'" multiple="multiple" style="display: block">'+

            '</select>')

        $.ajax({
            type: 'POST',
            url: "/app_tower/host/searchHostByGrooupId",
            data: {
                groupId:$('#'+groupDivId).val(),
            },
            dataType: "json",
            success: function (data) {
                if (data.resultCode=="0087"){
                    alert(data.resultDesc);
                    top.location.href ='/login'
                }
                for (var i = 0; i < data.hostList.length; i++) {
                    $("#"+selectId).append("<option value='" + data.hostList[i].fields.NAME + "' selected>" + data.hostList[i].fields.NAME + "</option>");

                }
                $('#'+selectId).change(function() {
                    hosts.splice(0,hosts.length)
                    var arr=$(this).val()
                    for (var i=0;i<arr.length;i++){
                        hosts.push(arr[i])
                    }
                }).multipleSelect({
                    width: '62%',
                    filter:true
                });
            },
            error: function () {
                console.log("error");
            },
            complete: function (XMLHttpRequest, textStatus) {
                console.log("complete");
            }
        })

    }
}
function onRunSHGroupChange() {
    $("#chooseRunSHHost").html('')
    if ($('#runSH_group').val()=='0'){
        $('#runshIp').html("");
        $('#runshIp').append('<input type="text" class="form-control" placeholder="请输入ip"  id="writeRunSHHost"  style="display: block">')

        $('#writeRunSHHost').bind('input propertychange', function () {
            RunSH_hosts=[]
            RunSH_hosts.push($(this).val())
        })
        return;
    }else{
        $('#runshIp').html("");
        $('#runshIp').append('<select id="chooseRunSHHost" multiple="multiple" style="display: block">'+

                             '</select>')

    $.ajax({
        type: 'POST',
        url: "/app_tower/host/searchHostByGrooupId",
        data: {
            groupId:$('#runSH_group').val(),
        },
        dataType: "json",
        success: function (data) {
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }

            for (var i = 0; i < data.hostList.length; i++) {
                $("#chooseRunSHHost").append("<option value='" + data.hostList[i].fields.NAME + "' selected>" + data.hostList[i].fields.NAME + "</option>");

            }
            $('#chooseRunSHHost').change(function() {
                RunSH_hosts=$(this).val()
            }).multipleSelect({
                width: '62%',
                filter:true
            });
            console.log($('#chooseRunSHHost').val())

        },
        error: function () {
            console.log("error");
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })

    }
}
function onLOGGroupChange() {
    $("#chooseLOGHost").html('')

    if ($('#searchLog_group').val()=='0'){
        $('#logIp').html("");
        $('#logIp').append('<input type="text" class="form-control" placeholder="请输入ip"  id="writeLOGHost"  style="display: block">')

        $('#writeLOGHost').bind('input propertychange', function () {
            LOG_hosts=[]
            LOG_hosts.push($(this).val())
        })
        return;
    }else{
        $('#logIp').html("");
        $('#logIp').append('<select id="chooseLOGHost" multiple="multiple" style="display: block">'+

            '</select>')
    $.ajax({
        type: 'POST',
        url: "/app_tower/host/searchHostByGrooupId",
        data: {
            groupId:$('#searchLog_group').val(),
        },
        dataType: "json",
        success: function (data) {
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }

            for (var i = 0; i < data.hostList.length; i++) {
                $("#chooseLOGHost").append("<option value='" + data.hostList[i].fields.NAME + "' selected>" + data.hostList[i].fields.NAME + "</option>");

            }
            $('#chooseLOGHost').change(function() {
                LOG_hosts=$(this).val()
            }).multipleSelect({
                width: '62%',
                filter:true
            });
            console.log($('#chooseLOGHost').val())

        },
        error: function () {
            console.log("error");
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })
    }
}
function onCOPYGroupChange() {
    $("#chooseCOPYHost").html('')

    if ($('#copy_group').val()=='0'){
        $('#copyIp').html("");
        $('#copyIp').append('<input type="text" class="form-control" placeholder="请输入ip"  id="writeCOPYHost"  style="display: block">')

        $('#writeCOPYHost').bind('input propertychange', function () {
            CopyFile_hosts=[]
            CopyFile_hosts.push($(this).val())
        })
        return;
    }else {
        $('#copyIp').html("");
        $('#copyIp').append('<select id="chooseCOPYHost" multiple="multiple" style="display: block">' +

            '</select>')
        $.ajax({
            type: 'POST',
            url: "/app_tower/host/searchHostByGrooupId",
            data: {
                groupId: $('#copy_group').val(),
            },
            dataType: "json",
            success: function (data) {
                if (data.resultCode == "0087") {
                    alert(data.resultDesc);
                    top.location.href = '/login'
                }

                for (var i = 0; i < data.hostList.length; i++) {
                    $("#chooseCOPYHost").append("<option value='" + data.hostList[i].fields.NAME + "' selected>" + data.hostList[i].fields.NAME + "</option>");

                }
                $('#chooseCOPYHost').change(function () {
                    CopyFile_hosts = $(this).val()
                }).multipleSelect({
                    width: '62%',
                    filter: true
                });
                console.log($('#chooseCOPYHost').val())

            },
            error: function () {
                console.log("error");
            },
            complete: function (XMLHttpRequest, textStatus) {
                console.log("complete");
            }
        })
    }
}
function onSNGroupChange() {
    $("#chooseSNHost").html('')

    if ($('#searchSN_group').val()=='0'){
        $('#snIp').html("");
        $('#snIp').append('<input type="text" class="form-control" placeholder="请输入ip"  id="writeSNHost"  style="display: block">')

        $('#writeSNHost').bind('input propertychange', function () {
            SN_hosts=[]
            SN_hosts.push($(this).val())
        })
        return;
    }else {
        $('#snIp').html("");
        $('#snIp').append('<select id="chooseSNHost" multiple="multiple" style="display: block">' +

            '</select>')
        $.ajax({
            type: 'POST',
            url: "/app_tower/host/searchHostByGrooupId",
            data: {
                groupId: $('#searchSN_group').val(),
            },
            dataType: "json",
            success: function (data) {
                if (data.resultCode == "0087") {
                    alert(data.resultDesc);
                    top.location.href = '/login'
                }

                for (var i = 0; i < data.hostList.length; i++) {
                    $("#chooseSNHost").append("<option value='" + data.hostList[i].fields.NAME + "' selected>" + data.hostList[i].fields.NAME + "</option>");

                }
                $('#chooseSNHost').change(function () {
                    SN_hosts = $(this).val()
                }).multipleSelect({
                    width: '62%',
                    filter: true
                });
                console.log($('#chooseSNHost').val())

            },
            error: function () {
                console.log("error");
            },
            complete: function (XMLHttpRequest, textStatus) {
                console.log("complete");
            }
        })
    }
}
//执行sh脚本
function runSH() {
    var groupid = $('#runSH_group').val();
    var credentialsid = $('#runSH_credentials').val();
    var vars=$('#runSH_vars').val()
    if (groupid=='' || groupid==null || credentialsid=='' || credentialsid==null || vars==''||vars==null| RunSH_hosts.length==0){
        opt_commons.dialogShow("提示信息","请填写完整！",2000);
        return;
    }
    $.ajax({
        type: 'POST',
        url: "/app_tower/job/run_commands_runSH",
        data: {
            groupid: groupid,
            hostList:JSON.stringify(RunSH_hosts),
            credentialsid: credentialsid,
            vars:vars,
        },
        dataType: "json",
        success: function (data) {
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            if(data.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            if(data.resultCode=="0001"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            $('#taskid').val(data.taskid);
            $('#logfile').val(data.file);
            readLog(data.taskid, data.file)
        },
        error: function () {
            console.log("error");
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })
}
//查询进程
function searchProcess() {

    var credentialsid = $('#searchProcess_credentials').val();
    var processName=$('#searchProcess_processName').val();
    if (searchProcess_hosts.length==0 || credentialsid==null || credentialsid==''||processName==''||processName==null){
        opt_commons.dialogShow("提示信息","请填写完整！",2000);
        return;
    }

    $.ajax({
        type: 'POST',
        url: "/app_tower/job/run_commands_searchProcess",
        data: {
            hostList:JSON.stringify(searchProcess_hosts),
            credentialsid: credentialsid,
            processName:processName,
        },
        dataType: "json",
        success: function (data) {
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            if(data.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            if(data.resultCode=="0001"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            $('#taskid').val(data.taskid);
            $('#logfile').val(data.file);
            readLog(data.taskid, data.file)
        },
        error: function () {
            console.log("error");
                opt_commons.dialogShow("提示信息","错误！",2000);

        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })
}
//修改进程
function changeProcess() {

    var credentialsid = $('#changeProcess_credentials').val();
    var processName=$('#changeProcess_processName').val();
    var operation=$('#changeProcess_operation').val();
    if (changeProcess_hosts.length==0 || credentialsid==null || credentialsid==''||processName==''||processName==null||operation==''||operation==null){
        opt_commons.dialogShow("提示信息","请填写完整！",2000);
        return;
    }

    $.ajax({
        type: 'POST',
        url: "/app_tower/job/run_commands_changeProcess",
        data: {
            hostList:JSON.stringify(changeProcess_hosts),
            credentialsid: credentialsid,
            processName:processName,
            operation:operation,
        },
        dataType: "json",
        success: function (data) {
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            if(data.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            if(data.resultCode=="0001"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            $('#taskid').val(data.taskid);
            $('#logfile').val(data.file);
            readLog(data.taskid, data.file)
        },
        error: function () {
            console.log("error");
            opt_commons.dialogShow("提示信息","错误！",2000);

        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })
}
//增加/取消/查询权限
function changeAuth(action) {

    var credentialsid = $('#auth_credentials').val();
    var userName=$.trim($('#auth_userName').val());
    var port=$.trim($('#auth_port').val());
    var requestUser=$.trim($('#auth_requestUser').val());
    if (requestUser==null){
        requestUser=""
    }
    if (changeAuth_hosts.length==0){
        opt_commons.dialogShow("提示信息","主机不能为空！",2000);
        return;
    }
    if (userName=='root' ||  userName=='manage'){
        opt_commons.dialogShow("提示信息","不能修改root用户和manage用户",2000);
        return;
    }
    if ($('#auth_portCheckbox').val()){
        if (port=='' || port ==null){
            opt_commons.dialogShow("提示信息","请输入端口号",2000);
            return;
        }
    }
    if (action=='add' ||  action=='cancel'){
        if (requestUser=='' || requestUser==null){
            opt_commons.dialogShow("提示信息","修改权限时必须填写说明",2000);
            return;
        }

    }
    if (!$('#auth_portCheckbox').is(":checked")){
        port=22;
    }
    $.ajax({
        type: 'POST',
        url: "/app_tower/job/run_commands_changeSudoAuth",
        data: {
            hostList: JSON.stringify(changeAuth_hosts),
            credentialsid: credentialsid,
            userName:userName,
            action:action,
            port:port,
            requestUser:requestUser,
        },
        dataType: "json",
        success: function (data) {
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            if(data.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            if(data.resultCode=="0001"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            $('#taskid').val(data.taskid);
            $('#logfile').val(data.file);
            readLog(data.taskid, data.file)
        },
        error: function () {
            console.log("error");
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })
}

//查找SN号
function searchSN() {
    var groupid = $('#searchSN_group').val();
    var credentialsid = $('#searchSN_credentials').val();
    if (groupid=='' || groupid==null || credentialsid=='' || credentialsid==null || SN_hosts.length==0){
        opt_commons.dialogShow("提示信息","请填写完整！",2000);
        return;
    }
    $.ajax({
        type: 'POST',
        url: "/app_tower/job/run_commands_searchSN",
        data: {
            groupid: groupid,
            hostList:JSON.stringify(SN_hosts),
            credentialsid: credentialsid,
        },
        dataType: "json",
        success: function (data) {
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            if(data.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            $('#taskid').val(data.taskid);
            $('#logfile').val(data.file);
            readLog(data.taskid, data.file)
        },
        error: function () {
            console.log("error");
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })
}
//日志查询
function searchLog() {

    var groupid = $('#searchLog_group').val();
    var credentialsid = $('#searchLog_credentials').val();
    var cmd=$('#searchLog_cmd').val();
    var content=$('#searchLog_content').val();
    var path=$('#searchLog_filePath').val();
    if (groupid=='' || groupid==null || credentialsid=='' || credentialsid==null ||cmd=='' || cmd==null || content=='' || content==null || path=='' || path==null || LOG_hosts.length==0){
        opt_commons.dialogShow("提示信息","请填写完整！",2000);
        return;
    }
    $.ajax({
        type: 'POST',
        url: "/app_tower/job/run_commands_searchLog",
        data: {
            groupid: groupid,
            hostList:JSON.stringify(LOG_hosts),
            credentialsid: credentialsid,
            cmd:cmd,
            content:content,
            path:path,
        },
        dataType: "json",
        success: function (data) {
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            if(data.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            $('#taskid').val(data.taskid);
            $('#logfile').val(data.file);
            readLog(data.taskid, data.file)
        },
        error: function () {
            console.log("error");
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })
}
//分发文件
function copyFile(){
    var groupid = $('#copy_group').val();
    var credentialsid = $('#copy_credentials').val();
    var srcPath = $('#copy_srcPath').val();
    var desPath = $('#copy_desPath').val();
    if (groupid=='' || groupid==null || credentialsid=='' || credentialsid==null ||srcPath=='' || srcPath==null || desPath=='' || desPath==null  || CopyFile_hosts.length==0){
        opt_commons.dialogShow("提示信息","请填写完整！",2000);
        return;
    }
    $.ajax({
        type: 'POST',
        url: "/app_tower/job/run_commands_copyFile",
        data: {
            groupid: groupid,
            hostList:JSON.stringify(CopyFile_hosts),
            credentialsid: credentialsid,
            srcPath:srcPath,
            desPath:desPath,

        },
        dataType: "json",
        success: function (data) {
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            if(data.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            $('#taskid').val(data.taskid);
            $('#logfile').val(data.file);
            readCopyLog(data.taskid, data.file,desPath,groupid,credentialsid)
        },
        error: function () {
            console.log("error");
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })
}

function runCommands() {
    var commands = $('#commands').val();
    $.ajax({
        type: 'POST',
        url: "/app_tower/job/run_commands",
        data: {
            commands: commands,

        },
        dataType: "json",
        success: function (data) {
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            if(data.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            $('#taskid').val(data.taskid);
            $('#logfile').val(data.file);
            readLog(data.taskid, data.file)
        },
        error: function () {
            console.log("error");
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })
}
//读日志
function readLog(id, file) {
    var taskid = id;
    var logfile = file;
    seek();
    function seek() {
        $.ajax({
            type: 'POST',
            url: "/app_tower/job/read_commands_log",
            data: {
                taskid: taskid,
                logfile: logfile,
            },
            dataType: "json",
            success: function (data) {
                if (data.resultCode=="0087"){
                    alert(data.resultDesc);
                    top.location.href ='/login'
                }
                if(data.resultCode=="0057"){
                    opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                    return;
                }
                $('#log').val(data.log)
                $("#log").scrollTop($("#log")[0].scrollHeight);
                setTimeout(function () {
                    if (data.read_flag == 'True') {
                        $('#runAnimate').fadeToggle('slow');
                        seek();
                    }else{
                        $('#runAnimate').fadeOut('slow');
                    }
                }, 1000)
            },
            error: function () {
                $('#runAnimate').fadeOut('slow');
                console.log("error");
            },
            complete: function (XMLHttpRequest, textStatus) {
                console.log("complete");
            }
        })
    }


}

function runAnsible() {
    var groupid = $('#group').val();
    var credentialsid = $('#credentials').val();
    var commandName = $('#commandName').val();
    var vars = $('#vars').val();
    $.ajax({
        type: 'POST',
        url: "/app_tower/job/run_commands2",
        data: {
            groupid: groupid,
            credentialsid: credentialsid,
            commandName: commandName,
            vars: vars,
        },
        dataType: "json",
        success: function (data) {
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            if(data.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            $('#taskid').val(data.taskid);
            $('#logfile').val(data.file);
            readLog(data.taskid, data.file)
        },
        error: function () {
            console.log("error");
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })
}
//读分发文件日志
function readCopyLog(id, file,path,groupId,credentialsid) {
    var taskid = id;
    var logfile = file;
    var desPath=path;
    var groupid=groupId
    var   credentialsid=credentialsid
    seek();
    function seek() {
        $.ajax({
            type: 'POST',
            url: "/app_tower/job/read_commands_log",
            data: {
                taskid: taskid,
                logfile: logfile,
            },
            dataType: "json",
            success: function (data) {
                if (data.resultCode=="0087"){
                    alert(data.resultDesc);
                    top.location.href ='/login'
                }
                if(data.resultCode=="0057"){
                    opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                    return;
                }
                $('#log').val(data.log)
                $("#log").scrollTop($("#log")[0].scrollHeight);
                setTimeout(function () {
                    if (data.read_flag == 'True') {
                        seek();
                    }else{
                        //分发完毕，查看文件
                            $.ajax({
                                type: 'POST',
                                url: "/app_tower/job/checkFile",
                                data: {
                                    taskid: taskid,
                                    groupid:groupid,
                                    hostList:JSON.stringify(CopyFile_hosts),
                                    credentialsid:credentialsid,
                                    logfile: logfile,
                                    desPath:desPath,
                                },
                                dataType: "json",
                                success: function (data) {
                                    if (data.resultCode=="0087"){
                                        alert(data.resultDesc);
                                        top.location.href ='/login'
                                    }
                                    if(data.resultCode=="0057"){
                                        opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                                        return;
                                    }
                                    $('#taskid').val(data.taskid);
                                    $('#logfile').val(data.file);
                                    readLog(data.taskid, data.file)

                                },
                                error: function () {
                                    console.log("error");
                                },
                                complete: function (XMLHttpRequest, textStatus) {
                                    console.log("complete");
                                }})
                    }
                }, 1000)
            },
            error: function () {
                console.log("error");
            },
            complete: function (XMLHttpRequest, textStatus) {
                console.log("complete");
            }
        })
    }


}

function changepasswd() {
    //var goal_ip = $('#goal_ip').val();
    var changepwd_credentials = $('#changepwd_credentials').val();
    var new_pwd= $('#new_pwd').val();
    var try_pwd=$('#try_pwd').val();
    var user_name=$('#user_name').val();
    var re_ip= /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/;
    if (changepwd_hosts.length==0 ||changepwd_credentials==''||changepwd_credentials==null||new_pwd==''||new_pwd==null||try_pwd==''||try_pwd==null||user_name==''||user_name==null){
        opt_commons.dialogShow("提示信息","请填写完整！",2000);
        return;
    }
    // else if(re_ip.test(goal_ip)==false){
    //     opt_commons.dialogShow("提示信息","请填写正确的ip格式！",2000);
    //     return;
    // }
    else if(new_pwd!==try_pwd){
        opt_commons.dialogShow("提示信息","两次密码不相同",2000);
        return;
    }else if(user_name=='root' || user_name=='version'){
	opt_commons.dialogShow("提示信息","root/version用户无法修改",2000);
        return;
    }
    $.ajax({
        type: 'POST',
        url: "/app_tower/job/run_commands_change_passwd",
        data: {
            hostList:JSON.stringify(changepwd_hosts),
            changepwd_credentials:changepwd_credentials,
            new_pwd: new_pwd,
            user_name:user_name,
        },
        dataType: "json",
        success: function (data) {
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            if(data.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }else if(data.resultCode=="0058"){
                opt_commons.dialogShow("提示信息","请不要填写键盘连续字符4个",2000);
                return;
            }else if(data.resultCode=="0059"){
                opt_commons.dialogShow("提示信息","密码必须包含大写字母、小写字母、数字、标点",2000);
                return;
            }else if(data.resultCode=="0060"){
                opt_commons.dialogShow("提示信息","密码至少8位字符",2000);
                return;
            }
            $('#taskid').val(data.taskid);//taskid
            $('#logfile').val(data.file);//file
            readLog(data.taskid, data.file)
        },
        error: function () {
            console.log("error");
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })
}


//@ sourceURL=commands.js