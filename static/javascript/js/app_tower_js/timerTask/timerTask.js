/**
 * Created by PC on 2017/11/3.
 */
var selectionIds = [];  //保存选中ids
Array.prototype.removeByValue = function(val) {
    for(var i=0; i<this.length; i++) {
        if(this[i] == val) {
            this.splice(i, 1);
            break;
        }
    }
}
String.prototype.replaceAll = function (s1, s2) {
    return this.replace(new RegExp(s1, "gm"), s2);
}
$(function(){
    var oTable_timerTask = new TableInit_timerTask();
    oTable_timerTask.Init();


})

var TableInit_timerTask = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#timerTask_table').bootstrapTable({
            url: '/app_tower/timerTask/select',

            method:"GET",
            striped: true, //是否显示行间隔色
            cache: false, //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true, //是否显示分页（*）
            sortable: true, //是否启用排序
            sortOrder: "asc",
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server", //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1, //初始化加载第一页，默认第一页
            pageSize: 5, //每页的记录行数（*）
            pageList: [5, 20, 50, 100], //可供选择的每页的行数（*）
            strictSearch: true,
            showColumns: true, //是否显示所有的列
            showRefresh: true, //是否显示刷新按钮
            minimumCountColumns: 2, //最少允许的列数
            clickToSelect: false, //是否启用点击选中行
            height: 345, //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            showToggle:true, //是否显示详细视图和列表视图的切换按钮
            cardView: false, //是否显示详细视图
            detailView: false, //是否显示父子表
            onCheck: function (row) {
                //单行最前面的checkbox被选中
                console.log(row)
                if ($.inArray(row.pk, selectionIds)== -1){//不存在
                    selectionIds.push(row.pk);
                }
            },
            onUncheck: function (row) {
                //单行最前面的checkbox被取消
                console.log(row)
                if ($.inArray(row.pk, selectionIds)!= -1){//存在
                    selectionIds.removeByValue(row.pk)
                }


            },
            onCheckAll: function (rows) {
                //最顶上的checkbox被选中
                console.log(rows)
                for (var i=0;i<rows.length;i++){
                    if ($.inArray(rows[i].pk, selectionIds)== -1){//不存在
                        selectionIds.push(rows[i].pk)
                    }
                }
            },
            onUncheckAll: function (rows) {
                //最顶上的checkbox被取消
                console.log(rows)
                for (var i=0;i<rows.length;i++){
                    if ($.inArray(rows[i].pk, selectionIds)!= -1){//存在
                        selectionIds.removeByValue(rows[i].pk)
                    }
                }
            },
            responseHandler: function(res) { //返回数据处理
                if (res.resultCode=="0087"){
                    alert(res.resultDesc);
                    top.location.href ='/login'
                }
                if(res.resultCode=="0057"){
                    $('.fixed-table-loading').html(res.resultDesc)
                    return;
                }
                if(res.resultCode=="0001"){
                    opt_commons.dialogShow("提示信息",res.resultDesc,2000);
                    return;
                }
                var data=JSON.parse(res.rows);
                $.each(data, function (i, row) {
                    row.checkStatus = $.inArray(row.pk, selectionIds) != -1;  //判断当前行的数据id是否存在与选中的数组，存在则将多选框状态变为true
                });
                return {
                    "total": res.total,//总页数
                    "rows": data  //数据
                };
            },
            columns: [
                {field: 'checkStatus',checkbox: true},
                {
                    field: 'pk',
                    title: 'ID',
                    align : 'center',
                    sortable : true,
                    visible:true
                },
                {
                    field: 'fields.NAME',
                    title: '任务名称',
                    align : 'center',
                    sortable : true,
                    formatter:function(value, row, index){
                        return  value;
                        //'<a href="/static/templates/pages/jobTemplate_run.html?id='+row.pk+'&name='+row.fields.NAME+'">'+value+'</a>'
                    }

                },{
                    field: 'fields.DESCRIPTION',
                    title: '描述',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.ISUSE',
                    title: '是否启用',
                    align : 'center',
                    sortable : true,
                    formatter:function(value, row, index){

                        return  value;
                        //'<a href="/static/templates/pages/jobTemplate_run.html?id='+row.pk+'&name='+row.fields.NAME+'">'+value+'</a>'
                    }

                },{
                    field: 'fields.START_TIME',
                    title: '开始时间',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.EXPIRES_TIME',
                    title: '过期时间',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.EVERY',
                    title: '间隔',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.PERIOD',
                    title: '间隔单位',
                    align : 'center',
                    sortable : true

                }, {
                    field: 'fields.CREATE_USER_NAME',
                    title: '创建人',
                    align : 'center',
                    sortable : true

                }, {
                    field: 'fields.CREATE_TIME',
                    title: '创建时间',
                    align : 'center',
                    sortable : true

                }, {
                    title: '操作',
                    align : 'center',
                    sortable : true,
                    formatter:function(value, row, index){
                        var id=row.pk;
                        var data=JSON.stringify(row);
                        var stra=""
                        var strb=" <a class='btn btn-warning btn-xs' title=" + '编辑' +
                            " href='javascript:showUpdateTaskModal("+data+");'>" +
                            "<i class='ace-icon fa fa-pencil bigger-130'></i>编辑</a>" +
                            "  <a class='btn btn-danger btn-xs' title=" + '删除' +
                            " href='javascript:showDeleteTaskModal("+data+");'>" +
                            "<i class='ace-icon fa fa-trash-o bigger-130'></i>删除</a>";
                        var timeNow = parseInt(new Date().getTime());//当前时间
                        console.log(timeNow);
                        var expireDate = row.fields.EXPIRES_TIME.replaceAll('T',' ');
                        expireDate = expireDate.substring(0,19);
                        expireDate = expireDate.replace(/-/g,'/');
                        var expireDate = parseInt(new Date(expireDate).getTime());
                        console.log(expireDate);
                        if (timeNow > expireDate){
                            stra="<span class='label label-default'>"+"<i class='ace-icon fa fa-stop-circle-o bigger-130'></i>"+"过期"+"</span>"
                        }else{
                            if (row.fields.ISUSE){
                                stra=" <a class='btn btn-primary btn-xs' title=" + '停止' +
                                    " href='javascript:stopTimerTask("+id+");'>" +
                                    "<i class='ace-icon fa fa-stop-circle-o bigger-130'></i>停止</a>"
                            }else{
                                stra=" <a class='btn btn-success btn-xs' title=" + '启用' +
                                    " href='javascript:useTimerTask("+id+");'>" +
                                    "<i class='ace-icon fa fa-rocket bigger-130'></i>启用</a>"
                            }
                        }

                        var str=stra+strb
                        return str
                    }
                },
            ]
        });
    };

    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = { //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit, //页面大小
            offset: params.offset, //页码
            order: params.order,
            ordername: params.sort,
            name:$("#name").val().trim(),
            description:$("#description").val().trim(),
        };
        return temp;
    };
    return oTableInit;
};
function timerTasksearch(){
    $("#timerTask_table").bootstrapTable('refresh');
}

function timerTasksearchReset(){
    $("#name").val("");
    $("#description").val("");

    timerTasksearch();
}

function showDeleteTaskModal(row){
    $('#deleteTaskModal').modal('show');
    $('#delete_id').val(row.pk);
    $('#deleteName').html(row.fields.NAME);
    $('#deleteDescription').html(row.fields.DESCRIPTION);
    $('#deleteIsUse').html(row.fields.ISUSE);
    $('#deleteStartTime').html(row.fields.START_TIME);
    $('#deleteEvery').html(row.fields.EVERY);
    $('#deletePeriod').html(row.fields.PERIOD);
    $('#deleteExpiresTime').html(row.fields.EXPIRES_TIME);

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
            $('#deleteJobTemplete').html("")
            for (var i=0;i<data.jobTempleteList.length;i++){
                if (data.jobTempleteList[i].pk==row.fields.JOBTEMPLETE_ID){
                    $('#deleteJobTemplete').html(data.jobTempleteList[i].fields.NAME)
                    return;
                }
            }
        },
        error: function(data) {
            console.log('error')
        }
    })
    if (row.fields.OWNER_ID){
        $("#deleteOwner").html('仅自己');
    }else if(row.fields.OWNER_ALL){
        $("#deleteOwner").html('所有人');
    }else if (row.fields.OWNER_PROJECT_ID){

        $.ajax({
            url:"/app_tower/project/init_ProjectModal",
            type:"POST",
            data:{
                id:row.fields.OWNER_PROJECT_ID
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
                $("#delete_owner").html(data.projectName);
            },
            error: function(data) {
                console.log("error");
            },
        });
    }
}
function deleteTask() {
    var id=$("#delete_id").val();
    $.ajax({
        url:"/app_tower/timerTask/delete",
        type:"POST",
        data:{
            id:id
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
                opt_commons.dialogShow("失败信息",data.resultDesc,2000);
                return;
            }
            if(data.resultCode=="0000"){
                opt_commons.dialogShow("失败信息",data.resultDesc,2000);
                $("#timerTask_table").bootstrapTable('refresh');
                return;
            }
        },
        error: function(data) {

            console.log("error");
            $("#timerTask_table").bootstrapTable('refresh');

        },
    });
}

function showUpdateTaskModal(row) {

    $('#updateStartTime').datetimepicker({
        format: 'yyyy-mm-dd hh:ii:ss',
        locale: moment.locale('zh-cn'),
        language:"zh-CN"

    });
    $('#updateExpiresTime').datetimepicker({
        format: 'yyyy-mm-dd hh:ii:ss',
        locale: moment.locale('zh-cn'),
        language:"zh-CN"

    });
    $('#updateTaskModal').modal('show');
    $('#updateTask_id').val(row.pk);
    $('#updateName').val(row.fields.NAME);
    $('#updateDescription').val(row.fields.DESCRIPTION);
    if (row.fields.ISUSE){
        $('#updateIsUse').prop("checked", true);
    }else{
        $('#updateIsUse').prop("checked", false);
    }
    $('#updateStartTime').val(row.fields.START_TIME!=null ? row.fields.START_TIME.replaceAll('T',' ') : '');
    $('#updateEvery').val(row.fields.EVERY);
    $('#updatePeriod').val(row.fields.PERIOD);
    $('#updateExpiresTime').val(row.fields.EXPIRES_TIME!=null ? row.fields.EXPIRES_TIME.replaceAll('T',' ') : '');
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
            $('#updateJobTemplete').html("")
            for (var i=0;i<data.jobTempleteList.length;i++){
                if (data.jobTempleteList[i].pk==row.fields.JOBTEMPLETE_ID){
                    $('#updateJobTemplete').append('<option value="'+data.jobTempleteList[i].pk+'" selected>'+data.jobTempleteList[i].fields.NAME+'</option>')
                }else{
                    $('#updateJobTemplete').append('<option value="'+data.jobTempleteList[i].pk+'">'+data.jobTempleteList[i].fields.NAME+'</option>')
                }
            }
        },
        error: function(data) {
            console.log('error')
        }
    })
    $("#updateOwner").html('');
    $('#updateOwner').append('<option value="onlyOne" selected>'+'仅自己'+'</option>')
    $('#updateOwner').append('<option value="all" >'+'所有人'+'</option>')
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
            if(data.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }

            if (row.fields.OWNER_ID){
                $("#updateOwner").val('onlyOne');
            }else if(row.fields.OWNER_ALL){
                $("#updateOwner").val('all');
            }

            for (var i=0;i<data.projectList.length;i++){
                if (data.projectList[i].pk==row.fields.OWNER_PROJECT_ID){
                    $('#updateOwner').append('<option value="'+data.projectList[i].pk+'" selected>'+data.projectList[i].fields.NAME+'</option>')
                }else{
                    $('#updateOwner').append('<option value="'+data.projectList[i].pk+'" >'+data.projectList[i].fields.NAME+'</option>')
                }
            }
        },
        error: function(result) {
            console.log("error");
        },
    });
}
function updateTask() {
    opt_commons.query_validate("#update_Task_form");
    //校验不成功
    if (!$('#update_Task_form').valid()){
        return;
    }
    var timerTask_startTime=$('#updateStartTime').val()
    var timerTask_every=$('#updateEvery').val()
    if (timerTask_startTime!=null && timerTask_startTime!='' && timerTask_every!=null && timerTask_every!='' ){
        opt_commons.dialogShow("提示信息","开始时间与间隔时间二选一",2000);
        return
    }
    if ((timerTask_startTime==null || timerTask_startTime=='') && (timerTask_every==null || timerTask_every=='' )){
        opt_commons.dialogShow("提示信息","开始时间与间隔时间二选一",2000);
        return
    }
    $.ajax({
        url:"/app_tower/timerTask/update",
        type:"POST",
        data:{
            id:$('#updateTask_id').val(),
            NAME:$('#updateName').val(),
            DESCRIPTION:$('#updateDescription').val(),
            JOBTEMPLETE_ID:$('#updateJobTemplete').val(),
            ISUSE:$('#updateIsUse').is(':checked'),
            START_TIME:$('#updateStartTime').val(),
            EVERY:$('#updateEvery').val(),
            PERIOD:$('#updatePeriod').val(),
            EXPIRES_TIME:$('#updateExpiresTime').val(),
            OWNER:$('#updateOwner').val(),
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
                opt_commons.dialogShow("成功信息","修改信息成功！",2000);
                $("#timerTask_table").bootstrapTable('refresh');
                return;
            }
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error",2000);
            $("#timerTask_table").bootstrapTable('refresh');

        },
    });
}
//停止定时任务
function stopTimerTask(id) {
    $.ajax({
        url:"/app_tower/timerTask/stop",
        type:"POST",
        data:{
            id:id,
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
                opt_commons.dialogShow("成功信息",data.resultDesc,2000);
                $("#timerTask_table").bootstrapTable('refresh');
                return;
            }
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error!",2000);
            $("#timerTask_table").bootstrapTable('refresh');

        },
    });
}
//启用定时任务
function useTimerTask(id) {
    $.ajax({
        url:"/app_tower/timerTask/start",
        type:"POST",
        data:{
            id:id,
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
                opt_commons.dialogShow("成功信息",data.resultDesc,2000);
                $("#timerTask_table").bootstrapTable('refresh');
                return;
            }
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error!",2000);
            $("#timerTask_table").bootstrapTable('refresh');

        },
    });
}

//@ sourceURL=timerTask.js