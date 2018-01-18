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
                var htmlstr=""
                for (var j=0;j<data.tools.length;j++){

                        var toolid="toolid"+data.tools[j].pk
                        htmlstr+='<div class="tool-item" id="'+toolid+'">'+
                            '<a class="tool-item-inner" id="toolId" href="/static/templates/pages/app_tower_pages/workingPlatform/toolDetail.html?toolid='+data.tools[j].pk+'&toolname='+data.tools[j].fields.NAME+'" >'+
                            '<div class="tool-item-icon">'+
                            '<i class=" orange2 ace-icon fa fa-pencil bigger-120" style="font-size:xx-large" aria-hidden="true"></i>'+
                            '</div>'+
                            '<div class="tool-item-name">'+data.tools[j].fields.NAME+'</div>'+
                            '</a>'+
                             '<div class="row" style="height: 20px;overflow:hidden;margin-top: 10px"><span class="col-md-4" >'+data.tools[j].fields.CREATE_USER_NAME+'</span><span style="border-left:1px solid #cdcdcd;border-right: 1px solid #cdcdcd" class="col-md-4">'+data.tools[j].fields.ARGS1+'</span><span class="col-md-4">'+data.tools[j].fields.CREATE_TIME.slice(0,10)+'</span></div>'+
                            '<div class="row" style="height: 80px;overflow:hidden;margin: 5px">'+data.tools[j].fields.DESCRIPTION+'</div>'+
                            '<button type="button" style="width: 100px" onclick="importTool('+data.tools[j].pk+')" class="btn btn-hover btn-default ng-scope">导入</button>'+
                            '</div>'

                }
                $('#tool-panel').append(htmlstr)
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