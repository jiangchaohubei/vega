/**
 * Created by PC on 2017/8/17.
 */
$(function () {

    opt_commons.query_validate("#timerTask_form");
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
                $('#timerTask_owner').append('<option value="'+data.projectList[i].pk+'">'+data.projectList[i].fields.NAME+'</option>')
            }
        },
        error: function(data) {
            console.log('error')
        }
    })
    $.ajax({
        url:"/app_tower/timerTask/init_jobTemplete_select",
        type:"POST",
        data:{
        },
        dataType:"json",
        success:function(data){
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            $('#timerTask_jobTemplete').html("")
            for (var i=0;i<data.jobTempleteList.length;i++){
                $('#timerTask_jobTemplete').append('<option value="'+data.jobTempleteList[i].pk+'">'+data.jobTempleteList[i].fields.NAME+'</option>')
            }
        },
        error: function(data) {
            console.log('error')
        }
    })

    $('#timerTask_startTime').datetimepicker({
        format: 'yyyy-mm-dd hh:ii:ss',
        locale: moment.locale('zh-cn'),
        language:"zh-CN"

    });
    $('#timerTask_expiresTime').datetimepicker({
        format: 'yyyy-mm-dd hh:ii:ss',
        locale: moment.locale('zh-cn'),
        language:"zh-CN"

    });



})
//保存定时任务
function save_timerTask(){
    //校验不成功
    if (!$('#timerTask_form').valid()){
        return;
    }

    var timerTask_name=$('#timerTask_name').val();
    var timerTask_desc=$('#timerTask_desc').val();
    var timerTask_jobTemplete=$('#timerTask_jobTemplete').val()
    var timerTask_isUse=$('#timerTask_isUse').is(':checked')
    var timerTask_startTime=$('#timerTask_startTime').val();
    var timerTask_every=$('#timerTask_every').val();
    if (timerTask_startTime!=null && timerTask_startTime!='' && timerTask_every!=null && timerTask_every!='' ){
        opt_commons.dialogShow("提示信息","开始时间与间隔时间二选一",2000);
        return
    }
    if ((timerTask_startTime==null || timerTask_startTime=='') && (timerTask_every==null || timerTask_every=='' )){
        opt_commons.dialogShow("提示信息","开始时间与间隔时间二选一",2000);
        return
    }
    var timerTask_period=$('#timerTask_period').val();
    var timerTask_expiresTime=$('#timerTask_expiresTime').val();
    if (timerTask_expiresTime==null || timerTask_expiresTime==''){
        opt_commons.dialogShow("提示信息","过期时间必填",2000);
        return
    }
    var timerTask_owner=$('#timerTask_owner').val();


    $.ajax({
        url:"/app_tower/timerTask/add",
        type:"POST",
        data:{
            timerTask_name:timerTask_name,
            timerTask_desc:timerTask_desc,
            timerTask_jobTemplete:timerTask_jobTemplete,
            timerTask_isUse:timerTask_isUse,
            timerTask_startTime:timerTask_startTime,
            timerTask_every:timerTask_every,
            timerTask_period:timerTask_period,
            timerTask_expiresTime:timerTask_expiresTime,
            timerTask_owner:timerTask_owner,

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

                opt_commons.dialogShow("成功信息","添加成功！",2000);
                $('#timerTask_form')[0].reset();  //通过调用 DOM 中的reset方法来重置表单
                return;
            }
        },
        error: function(data) {
                opt_commons.dialogShow("提示信息","添加失败！",2000);
                console.log("error");
                return;
        },
    })

}






//@ sourceURL=timerTask_create.js