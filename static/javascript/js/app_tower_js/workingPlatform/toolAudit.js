/**
 * Created by PC on 2018/1/12.
 */

function onload_toolAudit() {
    //textarea全屏
    $('#tool_scriptcode').textareafullscreen();
    var C1 = window.location.href.split("?")[1];
    var C2 = C1.split("&");
    var toolid = C2[0].split("=")[1]
    var toolname = decodeURI(C2[1].split("=")[1])
    $('#toolname').html(toolname)
    $('#toolid').val(toolid)


    $.ajax({
        url:"/app_tower/workingPlatform/toolDetail_init",
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
                $('#tool_name').html(data.tool.NAME)
                var iconColor='green'
                switch(data.tool.DANGER_LEVEL)
                {
                    case 'safe':
                        iconColor='#4bd126';
                        break;
                    case 'middling':
                        iconColor='#31719f';
                        break;
                    case 'danger':
                        iconColor='#ff0016';
                        break;
                    default:
                        iconColor='green';
                }
                $('#toolIcon').html('<i class="'+data.tool.ICON+'" style="font-size:xx-large;line-height: 100px;height: 100px;color:'+iconColor+'" aria-hidden="true"></i>')
                $('#tool_creater').html(data.tool.CREATE_USER_NAME)
                $('#tool_desc').html(data.tool.DESCRIPTION)
                $('#tool_type').html(data.tool.ARGS1)
                if ( data.tool.SCRIPT_LANGUAGE==0){
                    $('#tool_language').html('shell')
                }else if (data.tool.SCRIPT_LANGUAGE==1){
                    $('#tool_language').html('python')
                }else{
                    $('#tool_language').html('yaml')
                }

                $('#tool_scriptcode').html(data.tool.SCRIPT_CODE)
                $('#tool_owner').html(data.tool.ARGS2)
                var inputs=""
                var outputs=""
                for (var i=0;i<data.toolinput.length;i++){
                    inputs+=data.toolinput[i].fields.NAME+'&nbsp;&nbsp;&nbsp;&nbsp;'
                }
                for (var i=0;i<data.tooloutput.length;i++){
                    outputs+=data.tooloutput[i].fields.NAME+'&nbsp;&nbsp;&nbsp;&nbsp;'
                }
                $('#tool_input').html(inputs)
                $('#tool_output').html(outputs)
                return;
            }
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error",2000);


        },
    });
}

function audit(status) {
    var toolid=$('#toolid').val()
    var auditStaus=status
    var auditReason=""
    if (auditStaus==1){
        auditReason="审核通过"
    }else if (auditStaus==2){
        auditReason=$('#auditReason').val()
    }
    $.ajax({
        url:"/app_tower/workingPlatform/tool_audit",
        type:"POST",
        data:{
            toolid:toolid,
            auditStaus:auditStaus,
            auditReason:auditReason
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
                opt_commons.dialogShow("成功信息","审核成功！",2000);
                window.location.href='/static/templates/pages/app_tower_pages/workingPlatform/toolshop.html'
                return;
            }
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error",2000);


        },
    });

}

function deleteTool() {
    var toolid=$('#toolid').val()
    if(confirm("你确信要删除工具："+$('#toolname').html()+"？")){
        $.ajax({
            url:"/app_tower/workingPlatform/tool_delete",
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
                    opt_commons.dialogShow("成功信息","删除成功！",2000);
                    window.location.href='/static/templates/pages/app_tower_pages/workingPlatform/working.html'
                    return;
                }
            },

            error:function(data){
                opt_commons.dialogShow("错误信息","error",2000);


            },
        });
    }

}


//@ sourceURL=toolAudit.js