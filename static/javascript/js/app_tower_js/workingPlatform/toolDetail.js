/**
 * Created by PC on 2018/1/12.
 */

function onload_tooldetail() {
    //textarea全屏
    $('#tool_scriptcode').textareafullscreen();
    var C1 = window.location.href.split("?")[1];
    var C2 = C1.split("&");
    var toolid = C2[0].split("=")[1]
    var toolname = decodeURI(C2[1].split("=")[1])
    $('#toolname').html(toolname)
    $('#toolid').val(toolid)
    $('#runtoolbt').attr('href','/static/templates/pages/app_tower_pages/workingPlatform/runTool.html?toolid='+toolid+'&toolname='+toolname)
    $('#edittoolbt').attr('href','/static/templates/pages/app_tower_pages/workingPlatform/editTool.html?toolid='+toolid+'&toolname='+toolname)

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
                var a=/^glyphicon glyphicon-/;
                var iconHtml=''
                var b=data.tool.ICON;

                if (a.test(b)){
                    iconHtml='<i class="'+b+'" style="font-size:xx-large;line-height: 100px;height: 100px;color:'+iconColor+'" aria-hidden="true"></i>'
                }else{
                    iconHtml="<img src='/icons/img/"+b+"' style='width:32px;height:32px;line-height: 100px;height: 100px;color:'"+iconColor+"'>"
                }
                $('#toolIcon').html(iconHtml)
                $('#tool_name').html(data.tool.NAME)
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



//@ sourceURL=toolDetail.js