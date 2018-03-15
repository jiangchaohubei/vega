/**
 * Created by PC on 2018/1/15.
 */

function onload_runTool() {
    var C1 = window.location.href.split("?")[1];
    var C2 = C1.split("&");
    var toolid = C2[0].split("=")[1]
    var toolname = decodeURI(C2[1].split("=")[1])
    $('#toolname').html(toolname)
    $('#toolid').val(toolid)
    $('#toolDetail').attr('href','/static/templates/pages/app_tower_pages/workingPlatform/toolDetail.html?toolid='+toolid+'&toolname='+toolname)
    $('#toolDetail').html(toolname)
    $.ajax({
        url:"/app_tower/workingPlatform/runTool_init",
        type:"POST",
        data:{
            toolid:toolid
        },
        dataType:"json",
        success:function(data){
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
            if(data.resultCode=="0000"){
                for (var i=0;i<data.credentialsList.length;i++){
                    $('#runTool_credentials').append("<option value='" + data.credentialsList[i].pk + "'>" + data.credentialsList[i].fields.NAME + "</option>");
                }
                for (var i=0;i<data.toolinput.length;i++){
                    $('#inputList').append(
                        '<div >'+
                        '<label for="inventory" class="control-label col-md-2  requiredField" style="height:64px;line-height:50px;text-align:center">'+data.toolinput[i].fields.NAME+'</label>'+
                        '<div class="controls col-md-10" style="height:64px;">'+
                        '<input type="text" class="form-control" param_type="'+data.toolinput[i].fields.TYPE+'" value="'+data.toolinput[i].fields.DEFAULT+'" placeholder="'+data.toolinput[i].fields.DESCRIPTION+'" name="'+data.toolinput[i].fields.NAME+'" >&nbsp;'+
                        '</div>'+
                        ' </div>'
                    )
                }


                return;
            }
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error",2000);


        },
    });
}
//执行
function runTool() {

    $('#stopbtn').css('display', 'block');
    var toolid=$('#toolid').val();
    var hoststr=$('#choosed_hosts').val()
    console.log(hoststr)
    var hostList=hoststr.split(',')
    console.log(hostList)
    if (!hostList[hostList.length-1]){
        console.log(hostList)
        hostList.pop()
    }
    var inputParams=[]
    $('#inputList input').each(function (n,v) {
        var input={}
        var name=$(v).attr('name')
        var type=$(v).attr('param_type')
        var value=$(v).val()
        input['name']=name
        input['value']=value
        input['type']=type
        inputParams.push(input)
    })
    $.ajax({
        url:"/app_tower/workingPlatform/tool_run",
        type:"POST",
        data:{
            toolid:toolid,
            hostList:JSON.stringify(hostList),
            credentials:$('#runTool_credentials').val(),
            inputParams:JSON.stringify(inputParams),
        },
        dataType:"json",
        success:function(data){
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            if(data.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            if(data.resultCode=="0001"){
                console.log(data.resultCode)
                opt_commons.dialogShow("失败信息",data.resultDesc,2000);
                return;
            }
            if(data.resultCode=="0000"){
                $("#mask").css("height", window.screen.availHeight );
                $("#mask").css("width",$(document).width());
                $("#mask").show();
                $("#run_status").html('执行中')
                $("#run_user").html(data.runUser)
                $("#run_toolName").html(data.toolName)
                $("#log_taskid").val(data.taskid)
                $("#log_logfile").val(data.logfile)
                $("#log_toolEventId").val(data.toolEventId)
                var inputParams=JSON.parse(data.inputParams)
                for (var i=0;i<inputParams.length;i++){
                    $('#showInputList').html('');
                    $('#showInputList').append(
                        '<div >'+
                        '<label for="inventory" class="control-label col-md-2  requiredField" style="height:64px;line-height:50px;text-align:center">'+inputParams[i].name+'</label>'+
                        '<div class="controls col-md-10" style="height:64px;">'+
                        '<input type="text" class="form-control" param_type="'+inputParams[i].type+'" value="'+inputParams[i].value+'"  name="'+inputParams[i].name+'" >&nbsp;'+
                        '</div>'+
                        '</div>'
                    )
                }

                var seek = 0;
                getlog(seek);
                function getlog(se) {
                    $.ajax({
                        type: 'POST',
                        url: "/app_tower/workingPlatform/read_log",
                        data: {
                            taskid: data.taskid,
                            logfile: data.logfile,
                            seek: se,
                            toolEventId: data.toolEventId,
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
                            console.log(data);
                            var result = data
                            seek = result.seek;
                            $('#run_log').val(result.log)
                            $('#run_status').html(result.state);
                            if (result.state == 'REVOKED' || result.state == 'SUCCESS' || result.state == 'FAILURE') {
                                $('#stopbtn').css('display', 'none');
                            }
                            if (result.state == 'REVOKED') {
                                $('#run_startTime').html("- - -");
                            } else if (result.toolEvent.startTime == 'null') {
                                $('#run_startTime').html("执行中");
                            } else {
                                $('#run_startTime').html(result.toolEvent.startTime.substring(1, result.toolEvent.startTime.length - 1));
                            }
                            if (result.state == 'REVOKED') {
                                $('#run_endTime').html("- - -");
                            } else if (result.toolEvent.endTime == 'null') {
                                $('#run_endTime').html("执行中");
                            } else {
                                $('#run_endTime').html(result.toolEvent.endTime.substring(1, result.toolEvent.endTime.length - 1));
                            }
                            if (result.state == 'REVOKED') {
                                $('#run_elapsed').html("- - -");
                            } else if (result.toolEvent.elapsed == 0) {
                                $('#run_elapsed').html(0);
                            } else if (!result.toolEvent.elapsed) {
                                $('#run_elapsed').html("执行中");
                            } else {
                                $('#run_elapsed').html(result.toolEvent.elapsed);
                            }


                            $("#run_log").scrollTop($("#run_log")[0].scrollHeight);
                            setTimeout(function () {
                                    if (result.read_flag == 'True') {
                                        getlog(seek)
                                    }else{
                                        event_sumarise_init($("#log_toolEventId").val())
                                    }}

                                , 1000)

                        },
                        error: function () {
                            console.log("error");
                        },
                        complete: function (XMLHttpRequest, textStatus) {
                            console.log("complete");
                        }
                    })
                }



                return;
            }
        },
        error: function(data) {

            opt_commons.dialogShow("错误","error",2000);
            console.log("error");

        },
    })
}
//概要统计
function event_sumarise_init(id) {

    var toolEventId = id;
    $.ajax({
        type: 'POST',
        url: "/app_tower/workingPlatform/get_event",
        data: {
            toolEventId: toolEventId
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

            eventList = data.eventList
            for (var i=0;i<eventList.length;i++){
                $('#eventTable').find('tbody').append(
                    '<tr>'+
                    '<td>'+eventList[i].fields.HOST_NAME+'</td>'+
                    '<td>'+eventList[i].fields.SUCCESS+'</td>'+
                    '<td>'+eventList[i].fields.FAILED+'</td>'+
                    '<td>'+eventList[i].fields.CHANGED+'</td>'+
                    '<td>'+eventList[i].fields.UNREACHABLE+'</td>'+
                    '<td>'+eventList[i].fields.SKIPPED+'</td>'+
                    '</tr>')
                // var str=''+eventList[i].fields.HOST_NAME+" ";
                // if (eventList[i].fields.SUCCESS!=0){
                //     str+='ok'+eventList[i].fields.SUCCESS+" ";
                // }
                // if (eventList[i].fields.FAILED!=0){
                //     str+='faield'+eventList[i].fields.FAILED+" ";
                // }
                // if (eventList[i].fields.CHANGED!=0){
                //     str+='changed'+eventList[i].fields.CHANGED+" ";
                // }
                // if (eventList[i].fields.UNREACHABLE!=0){
                //     str+='unreachable'+eventList[i].fields.UNREACHABLE+" ";
                // }
                // if (eventList[i].fields.SKIPPED!=0){
                //     str+='skipped'+eventList[i].fields.SKIPPED+" ";
                // }
                //
                // $('#backHostSelect').append('<option value="'+eventList[i].fields.HOST_ID+'">'+str+'</option>')
            }
            // //初始化双向列表
            // init_dualListbox();
            /*
             * 还要初始化主机组，凭证的下拉选择框
             *
             * */



        },
        error: function () {
            console.log("error");
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })
}

function stoprun() {
    var taskid = $('#log_taskid').val();
    var toolEventid = $('#log_toolEventId').val();
    $.ajax({
        type: 'POST',
        url: "/app_tower/workingPlatform/stop_tool",
        data: {
            taskid: taskid,
            toolEventId: toolEventid
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
            console.log(data);


        },
        error: function () {
            console.log("error");
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })
}



//模态框
function showCmdbModal(){

    $("#cmdbModal").modal("show");
    $.ajax({
        url:"/app_tower/host/init_cmdb_system",
        type:"POST",
        data:{

        },
        dataType:"json",
        success:function(data){
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            if(data.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            if(data.resultCode=="0000"){

                $('#cmdb_system').html('')
                $('#cmdb_system').append('<option value="all">所有系统</option>')

                for (var i=0;i<data.systemList.length;i++){
                    $('#cmdb_system').append('<option value="'+data.systemList[i].pk+'">'+data.systemList[i].fields.NAME+'</option>')
                }

            }
            if(data.resultCode=="0001"){
                opt_commons.dialogShow("失败信息",data.resultDesc,2000);

                return;
            }
        },
        error: function(data) {

            opt_commons.dialogShow("失败信息","error",2000);

        },
    });

    $.ajax({
        url:"/app_tower/host/selectBySomething",
        type:"POST",
        data:{
            system_id:'all',
            keyword:$('#cmdb_keyword').val(),
        },
        dataType:"json",
        success:function(data){
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            if(data.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            if(data.resultCode=="0000"){

                var str=""
                for (var i=0;i<data.hostList.length;i++){
                    str+='<tr>'+
                        '<td><label class="ui-checkbox"><input type="checkbox" readonly="" value="'+data.hostList[i].fields.NAME+'"><span></span></label></td>'+
                        ' <td class="text-may-ellipsis">'+data.hostList[i].pk+'</td>'+
                        ' <td class="text-may-ellipsis">'+data.hostList[i].fields.NAME+'</td>'+
                        '<td class="text-may-ellipsis" style="max-width: 224px;">'+data.hostList[i].fields.DESCRIPTION+'</td>'+
                        '<td class="text-may-ellipsis" style="max-width: 224px;">'+data.hostList[i].fields.MACHINE_TYPE+'</td>'+
                        '<td class="text-may-ellipsis" style="max-width: 224px;">'+data.hostList[i].fields.MACHINE_ROOM+'</td>'+
                        '</tr>'
                }
                $('#cmdb_tbody').html('')
                $('#cmdb_tbody').append(str)

            }
            if(data.resultCode=="0001"){
                opt_commons.dialogShow("失败信息",data.resultDesc,2000);

                return;
            }
        },
        error: function(data) {

            opt_commons.dialogShow("失败信息","error",2000);

        },
    });


}

function search_cmdb() {
    $.ajax({
        url:"/app_tower/host/selectBySomething",
        type:"POST",
        data:{
            system_id:$('#cmdb_system').val(),
            keyword:$('#cmdb_keyword').val(),
        },
        dataType:"json",
        success:function(data){
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            if(data.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            if(data.resultCode=="0000"){

                var str=""
                for (var i=0;i<data.hostList.length;i++){
                    str+='<tr>'+
                        '<td><label class="ui-checkbox"><input type="checkbox"  value="'+data.hostList[i].fields.NAME+'"><span></span></label></td>'+
                        ' <td class="text-may-ellipsis">'+data.hostList[i].pk+'</td>'+
                        ' <td class="text-may-ellipsis">'+data.hostList[i].fields.NAME+'</td>'+
                        '<td class="text-may-ellipsis" style="max-width: 224px;">'+data.hostList[i].fields.DESCRIPTION+'</td>'+
                        '<td class="text-may-ellipsis" style="max-width: 224px;">'+data.hostList[i].fields.MACHINE_TYPE+'</td>'+
                        '<td class="text-may-ellipsis" style="max-width: 224px;">'+data.hostList[i].fields.MACHINE_ROOM+'</td>'+
                        '</tr>'
                }
                $('#cmdb_tbody').html('')
                $('#cmdb_tbody').append(str)

            }
            if(data.resultCode=="0001"){
                opt_commons.dialogShow("失败信息",data.resultDesc,2000);

                return;
            }
        },
        error: function(data) {

            opt_commons.dialogShow("失败信息","error",2000);

        },
    });
}

function beSureChoose() {
    var ips=""
    $('#cmdb_tbody').find('input').each(function (n,v) {
        if ($(v).is(":checked")){
            ips+=$(v).val()+","
        }

    })
    $('#choosed_hosts').val(ips)
}

function closeRunModal(){
    $("#mask").hide();
}
function showRunModal() {
    $("#mask").css("height", window.screen.availHeight);
    $("#mask").css("width",$(document).width());
    $("#mask").show();
}

function showInputparam() {
    $('#showInputList').toggle();
}



//@ sourceURL=runTool.js