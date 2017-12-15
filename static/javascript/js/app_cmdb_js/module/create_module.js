/**
 * Created by PC on 2017/8/17.
 */
$(function () {

    opt_commons.query_validate("#module_form");
    $.ajax({
        url:"/app_tower/project/init_project_select",
        type:"POST",
        data:{

        },
        dataType:"json",
        success:function(data){
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            for (var i=0;i<data.projectList.length;i++){
                $('#MODULE_OWNER').append('<option value="'+data.projectList[i].pk+'">'+data.projectList[i].fields.NAME+'</option>')
            }

        },
        error: function(data) {
            console.log('error')
        }

    })
    $.ajax({
        url:"/app_cmdb/system/init_system_select",
        type:"POST",
        data:{

        },
        dataType:"json",
        success:function(data){
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            for (var i=0;i<data.systemList.length;i++){
                $('#MODULE_SYSTEM_ID').append('<option value="'+data.systemList[i].pk+'">'+data.systemList[i].fields.NAME+'</option>')
            }

        },
        error: function(data) {
            console.log('error')
        }

    })
})
function save_module(){
    //校验不成功
    if (!$('#module_form').valid()){
        return;
    }

    $.ajax({
        url:"/app_cmdb/module/add",
        type:"POST",
        data:{
            NAME:$('#MODULE_NAME').val(),
            DESCRIPTION:$('#MODULE_DESCRIPTION').val(),
            RESPONSIBLE_PERSON:$('#MODULE_RESPONSIBLE_PERSON').val(),
            OWNER:$('#MODULE_OWNER').val(),
            SYSTEM_ID:$('#MODULE_SYSTEM_ID').val(),


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
                opt_commons.dialogShow("失败",data.resultDesc,2000);
                return;
            }
            if(data.resultCode=="0000"){
                console.log(data.resultCode)
                opt_commons.dialogShow("成功信息","添加成功！",2000);
                $('#module_form')[0].reset();  //通过调用 DOM 中的reset方法来重置表单
                return;
            }
        },
        error: function(data) {
            console.log(data)
                opt_commons.dialogShow("错误",data.status+":"+data.statusText,2000);
        },
    })

}






//@ sourceURL=create_module.js