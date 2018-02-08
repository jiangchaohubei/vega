/**
 * Created by PC on 2018/1/15.
 */

$(function () {


    var C1 = window.location.href.split("?")[1];
    var C2 = C1.split("&");
    var toolEventId = C2[0].split("=")[1]
    var toolEventName = decodeURI(C2[1].split("=")[1])
    $('#toolEventName').val(toolEventName)
    $('#toolEventId').val(toolEventId)
    init(toolEventId);

})

function reRun() {
    $('#stopbtn').css('display', 'block');
    $.ajax({
        url:"/app_tower/workingPlatform/tool_reRun",
        type:"POST",
        data:{
            toolEventId:$('#toolEventId').val(),

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
                $('#toolEventId').val(data.toolEventId)
                init(data.toolEventId);

                return;
            }
        },
        error: function(data) {

            opt_commons.dialogShow("错误","error",2000);
            console.log("error");

        },
    })
}
//执行
function init(toolEventId) {

    $.ajax({
        url:"/app_tower/workingPlatform/toolEvent_init",
        type:"POST",
        data:{
            toolEventId:toolEventId,

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

                $("#run_status").html(data.toolEvent.STATUS)
                $("#run_user").html(data.toolEvent.CREATE_USER_NAME)
                $("#run_toolName").html(data.toolEvent.ARGS1)
                $("#log_taskid").val(data.toolEvent.CELERY_TASK_ID)
                $("#log_logfile").val(data.toolEvent.LOGFILE)
                $("#log_toolEventId").val(data.toolEvent.id)
                var inputParams=JSON.parse(data.toolEvent.INPUTPARAMS)
                console.log(inputParams)
                for (var i=0;i<inputParams.length;i++){
                    $('#showInputList').html('')
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
                getlog(data.toolEvent.CELERY_TASK_ID,data.toolEvent.LOGFILE);


                return;
            }
        },
        error: function(data) {

            opt_commons.dialogShow("错误","error",2000);
            console.log("error");

        },
    })
}
function getlog(taskid,logfile) {
    $.ajax({
        type: 'POST',
        url: "/app_tower/workingPlatform/read_log",
        data: {
            taskid: taskid,
            logfile: logfile,
            seek: 0,
            toolEventId: $("#log_toolEventId").val(),
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
                        getlog($("#log_taskid").val(), $("#log_logfile").val())
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





function showInputparam() {
    $('#showInputList').toggle();
}



//@ sourceURL=historyDetail.js