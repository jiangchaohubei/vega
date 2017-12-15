/**
 * Created by PC on 2017/8/17.
 */
$(function () {

    opt_commons.query_validate("#software_form");
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
                $('#SOFTWARE_OWNER').append('<option value="'+data.projectList[i].pk+'">'+data.projectList[i].fields.NAME+'</option>')
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
                $('#SOFTWARE_SYSTEM_ID').append('<option value="'+data.systemList[i].pk+'">'+data.systemList[i].fields.NAME+'</option>')
            }

            $.ajax({
                url:"/app_cmdb/software/init_system_module_select",
                type:"POST",
                data:{
                    systemId: $('#SOFTWARE_SYSTEM_ID').val()
                },
                dataType:"json",
                success:function(data){
                    if (data.resultCode=="0087"){
                        alert(data.resultDesc);
                        top.location.href ='/login'
                    }
                    for (var i=0;i<data.moduleList.length;i++){
                        $('#SOFTWARE_MODULE_ID').append('<option value="'+data.moduleList[i].pk+'">'+data.moduleList[i].fields.NAME+'</option>')
                    }

                },
                error: function(data) {
                    console.log('error')
                }

            })

        },
        error: function(data) {
            console.log('error')
        }

    })
})
function save_software(){
    //校验不成功
    if (!$('#software_form').valid()){
        return;
    }

    $.ajax({
        url:"/app_cmdb/software/add",
        type:"POST",
        data:{
            NAME:$('#SOFTWARE_NAME').val(),
            DESCRIPTION:$('#SOFTWARE_DESCRIPTION').val(),
            RESPONSIBLE_PERSON:$('#SOFTWARE_RESPONSIBLE_PERSON').val(),
            OWNER:$('#SOFTWARE_OWNER').val(),
            MODULE_ID:$('#SOFTWARE_MODULE_ID').val(),
            LISTEN_PORT:$('#SOFTWARE_LISTEN_PORT').val(),
            DEPLOY_DIR:$('#SOFTWARE_DEPLOY_DIR').val(),
            DEPLOY_ACCOUNT:$('#SOFTWARE_DEPLOY_ACCOUNT').val(),
            TIMER_SCRIPT:$('#SOFTWARE_TIMER_SCRIPT').val(),
            LOG_EXPORT:$('#SOFTWARE_LOG_EXPORT').val(),
            NOTE:$('#SOFTWARE_NOTE').val(),
            DATA_BACKUPPATH:$('#SOFTWARE_DATA_BACKUPPATH').val(),
            DATA_FILEPATH:$('#SOFTWARE_DATA_FILEPATH').val(),


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
                $('#software_form')[0].reset();  //通过调用 DOM 中的reset方法来重置表单
                return;
            }
        },
        error: function(data) {

                opt_commons.dialogShow("错误",data.status+":"+data.statusText,2000);
        },
    })

}

function onSystemChange() {
    $('#SOFTWARE_MODULE_ID').html('')
    $.ajax({
        url:"/app_cmdb/software/init_system_module_select",
        type:"POST",
        data:{
            systemId: $('#SOFTWARE_SYSTEM_ID').val()
        },
        dataType:"json",
        success:function(data){
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            for (var i=0;i<data.moduleList.length;i++){
                $('#SOFTWARE_MODULE_ID').append('<option value="'+data.moduleList[i].pk+'">'+data.moduleList[i].fields.NAME+'</option>')
            }

        },
        error: function(data) {
            console.log('error')
        }

    })
}






//@ sourceURL=create_software.js