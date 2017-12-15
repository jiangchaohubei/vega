/**
 * Created by PC on 2017/8/17.
 */
$(function () {

    opt_commons.query_validate("#host_form");
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
                $('#HOST_OWNER').append('<option value="'+data.projectList[i].pk+'">'+data.projectList[i].fields.NAME+'</option>')
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
                $('#HOST_SYSTEM_ID').append('<option value="'+data.systemList[i].pk+'">'+data.systemList[i].fields.NAME+'</option>')
            }

        },
        error: function(data) {
            console.log('error')
        }

    })
})
function save_host(){
    //校验不成功
    if (!$('#host_form').valid()){
        return;
    }

    $.ajax({
        url:"/app_cmdb/host/add",
        type:"POST",
        data:{
            NAME:$('#HOST_NAME').val(),
            DESCRIPTION:$('#HOST_DESCRIPTION').val(),
            VARIABLES:$('#HOST_VARIABLES').val(),
            OWNER:$('#HOST_OWNER').val(),
            MACHINE_TYPE:$('#HOST_MACHINE_TYPE').val(),
            MACHINE_ROOM:$('#HOST_MACHINE_ROOM').val(),
            MACHINE_POSITION:$('#HOST_MACHINE_POSITION').val(),
            CUTTER_NUMBER:$('#HOST_CUTTER_NUMBER').val(),
            SN_NUMBER:$('#HOST_SN_NUMBER').val(),
            OS:$('#HOST_OS').val(),
            PHYSICAL_MACHINE_TYPE:$('#HOST_PHYSICAL_MACHINE_TYPE').val(),
            NOTE:$('#HOST_NOTE').val(),
            SYSTEM_ID:$('#HOST_SYSTEM_ID').val(),

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
                $('#host_form')[0].reset();  //通过调用 DOM 中的reset方法来重置表单
                return;
            }
        },
        error: function(data) {
            console.log(data)
                opt_commons.dialogShow("错误",data.status+":"+data.statusText,2000);
        },
    })

}






//@ sourceURL=create_host.js