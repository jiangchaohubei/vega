/**
 * Created by PC on 2018/1/12.
 */

function onload_toolshop() {
    $.ajax({
        url:"/app_tower/workingPlatform/toolshop_init",
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
            if(data.resultCode=="0001"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            if(data.resultCode=="0000"){
                var htmlstr_audited=""
                for (var j=0;j<data.tools_audited.length;j++){
                    var iconColor='green'
                    switch(data.tools_audited[j].fields.DANGER_LEVEL)
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
                    var toolid="toolid"+data.tools_audited[j].pk
                    var hasImport=false;
                    for (t in data.toolimported){
                        if (data.toolimported[t].pk ==data.tools_audited[j].pk ){
                            hasImport=true
                        }
                    }
                    if (hasImport){//存在
                        htmlstr_audited+='<div class="tool-item" id="'+toolid+'">'+
                            '<a class="tool-item-inner" id="toolId" href="/static/templates/pages/app_tower_pages/workingPlatform/toolAudit.html?toolid='+data.tools_audited[j].pk+'&toolname='+data.tools_audited[j].fields.NAME+'" >'+
                            '<div class="tool-item-icon">'+
                            '<i class="'+data.tools_audited[j].fields.ICON+'" style="font-size:xx-large;color:'+iconColor+'" aria-hidden="true"></i>'+
                            '</div>'+
                            '<div class="tool-item-name">'+data.tools_audited[j].fields.NAME+'</div>'+
                            '</a>'+
                            '<div class="row" style="height: 20px;overflow:hidden;margin-top: 10px"><span class="col-md-4" >'+data.tools_audited[j].fields.CREATE_USER_NAME+'</span><span style="border-left:1px solid #cdcdcd;border-right: 1px solid #cdcdcd" class="col-md-4">'+data.tools_audited[j].fields.ARGS1+'</span><span class="col-md-4">'+data.tools_audited[j].fields.CREATE_TIME.slice(0,10)+'</span></div>'+
                            '<div class="row" style="height: 80px;overflow:hidden;margin: 5px">'+data.tools_audited[j].fields.DESCRIPTION+'</div>'+
                            '<button type="button" style="width: 100px" disabled class="btn btn-hover btn-default ng-scope">已导入</button>'+
                            '</div>'
                    }else{
                        htmlstr_audited+='<div class="tool-item" id="'+toolid+'">'+
                            '<a class="tool-item-inner" id="toolId" href="/static/templates/pages/app_tower_pages/workingPlatform/toolAudit.html?toolid='+data.tools_audited[j].pk+'&toolname='+data.tools_audited[j].fields.NAME+'" >'+
                            '<div class="tool-item-icon">'+
                            '<i class="'+data.tools_audited[j].fields.ICON+'" style="font-size:xx-large;color:'+iconColor+'" aria-hidden="true"></i>'+
                            '</div>'+
                            '<div class="tool-item-name">'+data.tools_audited[j].fields.NAME+'</div>'+
                            '</a>'+
                            '<div class="row" style="height: 20px;overflow:hidden;margin-top: 10px"><span class="col-md-4" >'+data.tools_audited[j].fields.CREATE_USER_NAME+'</span><span style="border-left:1px solid #cdcdcd;border-right: 1px solid #cdcdcd" class="col-md-4">'+data.tools_audited[j].fields.ARGS1+'</span><span class="col-md-4">'+data.tools_audited[j].fields.CREATE_TIME.slice(0,10)+'</span></div>'+
                            '<div class="row" style="height: 80px;overflow:hidden;margin: 5px">'+data.tools_audited[j].fields.DESCRIPTION+'</div>'+
                            '<button type="button" style="width: 100px" onclick="importTool('+data.tools_audited[j].pk+')" class="btn btn-hover btn-success ng-scope">导入</button>'+
                            '</div>'
                    }



                }
                $('#tool-panel').append(htmlstr_audited)
                $('#tool-span').html(data.tools_audited.length)


                var htmlstr_notaudited=""
                for (var j=0;j<data.tools_notaudited.length;j++){
                    var iconColor='green'
                    switch(data.tools_notaudited[j].fields.DANGER_LEVEL)
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
                    var toolid="toolid"+data.tools_notaudited[j].pk
                    htmlstr_notaudited+='<div class="tool-item" id="'+toolid+'">'+
                        '<a class="tool-item-inner" id="toolId" href="/static/templates/pages/app_tower_pages/workingPlatform/toolAudit.html?toolid='+data.tools_notaudited[j].pk+'&toolname='+data.tools_notaudited[j].fields.NAME+'" >'+
                        '<div class="tool-item-icon">'+
                        '<i class="'+data.tools_notaudited[j].fields.ICON+'" style="font-size:xx-large;color:'+iconColor+'" aria-hidden="true"></i>'+
                        '</div>'+
                        '<div class="tool-item-name">'+data.tools_notaudited[j].fields.NAME+'</div>'+
                        '</a>'+
                        '<div class="row" style="height: 20px;overflow:hidden;margin-top: 10px"><span class="col-md-4" >'+data.tools_notaudited[j].fields.CREATE_USER_NAME+'</span><span style="border-left:1px solid #cdcdcd;border-right: 1px solid #cdcdcd" class="col-md-4">'+data.tools_notaudited[j].fields.ARGS1+'</span><span class="col-md-4">'+data.tools_notaudited[j].fields.CREATE_TIME.slice(0,10)+'</span></div>'+
                        '<div class="row" style="height: 80px;overflow:hidden;margin: 5px">'+data.tools_notaudited[j].fields.DESCRIPTION+'</div>'+
                        '<span  style="width: 100px"  class="label label-info">未审核</span>'+
                        '</div>'

                }
                $('#tool-notaudited-panel').append(htmlstr_notaudited)
                $('#tool-notaudited-span').html(data.tools_notaudited.length)


                var htmlstr_failaudited=""
                for (var j=0;j<data.tools_failaudited.length;j++){
                    var iconColor='green'
                    switch(data.tools_failaudited[j].fields.DANGER_LEVEL)
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
                    var toolid="toolid"+data.tools_failaudited[j].pk
                    htmlstr_failaudited+='<div class="tool-item" id="'+toolid+'">'+
                        '<a class="tool-item-inner" id="toolId" href="/static/templates/pages/app_tower_pages/workingPlatform/toolAudit.html?toolid='+data.tools_failaudited[j].pk+'&toolname='+data.tools_failaudited[j].fields.NAME+'" >'+
                        '<div class="tool-item-icon">'+
                        '<i class="'+data.tools_failaudited[j].fields.ICON+'" style="font-size:xx-large;color:'+iconColor+'" aria-hidden="true"></i>'+
                        '</div>'+
                        '<div class="tool-item-name">'+data.tools_failaudited[j].fields.NAME+'</div>'+
                        '</a>'+
                        '<div class="row" style="height: 20px;overflow:hidden;margin-top: 10px"><span class="col-md-4" >'+data.tools_failaudited[j].fields.CREATE_USER_NAME+'</span><span style="border-left:1px solid #cdcdcd;border-right: 1px solid #cdcdcd" class="col-md-4">'+data.tools_failaudited[j].fields.ARGS1+'</span><span class="col-md-4">'+data.tools_failaudited[j].fields.CREATE_TIME.slice(0,10)+'</span></div>'+
                        '<div class="row" style="height: 80px;overflow:hidden;margin: 5px">'+data.tools_failaudited[j].fields.DESCRIPTION+'</div>'+
                        '<span  style="width: 100px"  class="label label-default">审核不通过</span>'+
                        '</div>'

                }
                $('#tool-failaudited-panel').append(htmlstr_failaudited)
                $('#tool-failaudited-span').html(data.tools_failaudited.length)
                return;
            }
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error",2000);


        },
    });
}

function importTool(toolId) {
    $.ajax({
        url:"/app_tower/workingPlatform/importTool",
        type:"POST",
        data:{
            toolId:toolId
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
                opt_commons.dialogShow("成功信息","导入成功！",2000);
                window.location.href='/static/templates/pages/app_tower_pages/workingPlatform/working.html'
                return;
            }
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error",2000);


        },
    });
}



//@ sourceURL=toolshop.js