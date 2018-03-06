/**
 * Created by PC on 2018/1/9.
 */

$(function () {
    $.ajax({
        url:"/app_tower/workingPlatform/working_init",
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
                var htmlstr=""
                for(var i=0;i<data.toolType.length;i++){
                    var tooltypehtml=""
                    var typeid="toolType"+data.toolType[i].pk
                    tooltypehtml+='<div class="tool-type row" id="'+typeid+'">'+
                            '<h3><strong>'+
                        '<div class="tool-type-name">'+data.toolType[i].fields.NAME+'</div>'+
                            '</strong></h3>'+
                       ' <div class="tool-list" style="float: left">'
                    var nothastoolitem=true
                    for (var j=0;j<data.tools.length;j++){
                            if (data.tools[j].fields.TOOLTYPE_ID==data.toolType[i].pk){
                                nothastoolitem=false;
                                var toolid="toolid"+data.tools[j].pk
                                var iconColor='green'
                                switch(data.tools[j].fields.DANGER_LEVEL)
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
                                var a=/^glyphicon  glyphicon-/
                                var iconHtml=''
                                if (a.test(data.tools[j].fields.ICON)){
                                    iconHtml='<i class="'+data.tools[j].fields.ICON+'" style="font-size:xx-large;color:'+iconColor+'" aria-hidden="true"></i>'
                                }else{
                                    iconHtml="<img src='/icons/img/"+data.tools[j].fields.ICON+"' style='width:32px;height:32px;color:'"+iconColor+"\'>"
                                }
                                tooltypehtml+='<div class="tool-item" id="'+toolid+'">'+
                                        '<span class="close red ace-icon fa fa-times bigger-120" title="移除工具" onclick="removeTool('+data.tools[j].pk+')" style="" aria-hidden="true"></span>'+
                                        '<a class="tool-item-inner" id="toolId" href="/static/templates/pages/app_tower_pages/workingPlatform/toolDetail.html?toolid='+data.tools[j].pk+'&toolname='+data.tools[j].fields.NAME+'" >'+
                                        '<div class="tool-item-icon">'+
                                        '<i class="'+data.tools[j].fields.ICON+'" style="font-size:xx-large;color:'+iconColor+'" aria-hidden="true"></i>'+
                                        '</div>'+
                                        '<div class="tool-item-name">'+data.tools[j].fields.NAME+'</div>'+
                                        '</a>'+
                                        '</div>'
                            }
                    }
                    tooltypehtml+='</div> </div>'
                    if (nothastoolitem){
                        tooltypehtml=""
                    }
                    htmlstr+=tooltypehtml

                }
                $('#tool-panel').append(htmlstr)
                return;
            }
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error",2000);


        },
    });

})

function removeTool(toolId) {
    $.ajax({
        url:"/app_tower/workingPlatform/removeTool",
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
                opt_commons.dialogShow("成功信息","移除成功！",2000);
                window.location.href='/static/templates/pages/app_tower_pages/workingPlatform/working.html'
                return;
            }
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error",2000);


        },
    });
}



//@ sourceURL=working.js