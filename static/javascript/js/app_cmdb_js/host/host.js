/**
 * Created by PC on 2017/7/14.
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
$(function(){
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
            $('#system').html('');
            $('#system').append('<option value="0" selected>所有系统</option>')
            for (var i=0;i<data.systemList.length;i++){
                $('#system').append('<option value="'+data.systemList[i].pk+'">'+data.systemList[i].fields.NAME+'</option>')
            }

            var oTable_inventories = new TableInit_inventories();
            oTable_inventories.Init();
        },
        error: function(data) {
            console.log('error')
        }

    })


})

var TableInit_inventories = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
       $('#host_table').bootstrapTable({
            url: '/app_cmdb/host/select',

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
                width:1,
                align : 'center',
                sortable : true,
                visible: true   //可见
            },
                {
                field: 'fields.NAME',
                title: '主机名称',
                align : 'center',
                sortable : true,


            },{
                field: 'fields.DESCRIPTION',
                title: '描述',
                align : 'center',
                sortable : true

            },{
                    field: 'fields.ARGS1',
                    title: '所属系统',
                    align : 'center',
                    sortable : true

                }, {
                    field: 'fields.MACHINE_TYPE',
                    title: '机器类型',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.MACHINE_ROOM',
                    title: '机房',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.MACHINE_POSITION',
                    title: '机架位置',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.CUTTER_NUMBER',
                    title: '刀框编号',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.SN_NUMBER',
                    title: 'SN号',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.OS',
                    title: 'OS',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.PHYSICAL_MACHINE_TYPE',
                    title: '物理机配置类型',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.NOTE',
                    title: '备注',
                    align : 'center',
                    sortable : true

                }, {
                //field: 'count',
                title: '操作',
                align : 'center',
                sortable : true,
                formatter:function(value, row, index){
                    var data=JSON.stringify(row);
                    return "<a class='btn btn-warning btn-xs' title=" + '编辑' +
            " href='javascript:updateHostModal(" + data + ");'>" +
            "<i class='ace-icon fa fa-pencil bigger-130'></i>编辑</a>" +
            "    <a  class='btn btn-danger btn-xs' title=" + '删除' +
            " href='javascript:showDeleteHostModal(" + data +");'>" +
            "<i class='ace-icon fa fa-trash-o bigger-130'></i>删除</a>";
                 }
            }, ]
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
            systemId:$("#system").val(),
        };
        return temp;
    };


return oTableInit;
};


 //删除主机组模态框
 function showDeleteHostModal(row){
     $('#deleteHostModal').modal('show');
     $('#delete_id').val(row.pk);
     $('#DELETE_SYSTEM_ID').html(row.fields.SYSTEM_ID);
     $('#DELETE_NAME').html(row.fields.NAME);
     $('#DELETE_DESCRIPTION').html(row.fields.DESCRIPTION);
     $('#DELETE_MACHINE_TYPE').html(row.fields.MACHINE_TYPE);
     $('#DELETE_MACHINE_ROOM').html(row.fields.MACHINE_ROOM);
     $('#DELETE_MACHINE_POSITION').html(row.fields.MACHINE_POSITION);
     $('#DELETE_CUTTER_NUMBER').html(row.fields.CUTTER_NUMBER);
     $('#DELETE_SN_NUMBER').html(row.fields.SN_NUMBER);
     $('#DELETE_OS').html(row.fields.OS);
     $('#DELETE_PHYSICAL_MACHINE_TYPE').html(row.fields.PHYSICAL_MACHINE_TYPE);
     $('#DELETE_NOTE').html(row.fields.NOTE);
     $('#DELETE_VARIABLES').html(row.fields.VARIABLES);
     if (row.fields.OWNER_ID){
         $("#DELETE_OWNER").html('仅自己');
     }else if(row.fields.OWNER_ALL){
         $("#DELETE_OWNER").html('所有人');
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
                 $("#DELETE_OWNER").html(data.projectName);
             },
             error: function(data) {
                 opt_commons.dialogShow("错误",data.status+":"+data.statusText,2000);
             },
         });
     }


}
 //删除主机组
function deleteHost(){
    var id=$("#delete_id").val();
     $.ajax({
       url:"/app_cmdb/host/delete",
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
           if(data.resultCode=="0000"){
                opt_commons.dialogShow("成功信息","删除信息成功！",2000);
               $("#host_table").bootstrapTable('refresh');
               return;
           }
           if(data.resultCode=="0001"){
               opt_commons.dialogShow("失败信息","删除失败，禁止删除！",2000);
               $("#host_table").bootstrapTable('refresh');
               return;
           }
       },
       error: function(data) {
              opt_commons.dialogShow("错误",data.status+":"+data.statusText,2000);

        },
   });
}

 //修改主机组模态框
function updateHostModal(row){
    $('#updateHostModal').modal('show');
    $('#updateHost_id').val(row.pk);
    $('#UPDATE_NAME').val(row.fields.NAME);
    $('#UPDATE_DESCRIPTION').val(row.fields.DESCRIPTION);
    $('#UPDATE_MACHINE_TYPE').val(row.fields.MACHINE_TYPE);
    $('#UPDATE_MACHINE_ROOM').val(row.fields.MACHINE_ROOM);
    $('#UPDATE_MACHINE_POSITION').val(row.fields.MACHINE_POSITION);
    $('#UPDATE_CUTTER_NUMBER').val(row.fields.CUTTER_NUMBER);
    $('#UPDATE_SN_NUMBER').val(row.fields.SN_NUMBER);
    $('#UPDATE_OS').val(row.fields.OS);
    $('#UPDATE_NOTE').val(row.fields.NOTE);
    $('#UPDATE_PHYSICAL_MACHINE_TYPE').val(row.fields.PHYSICAL_MACHINE_TYPE);
    $('#UPDATE_VARIABLES').val(row.fields.VARIABLES);

    $("#UPDATE_OWNER").html('');
    $('#UPDATE_OWNER').append('<option value="onlyOne" selected>'+'仅自己'+'</option>')
    $('#UPDATE_OWNER').append('<option value="all" >'+'所有人'+'</option>')
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
                $("#UPDATE_OWNER").val('onlyOne');
            }else if(row.fields.OWNER_ALL){
                $("#UPDATE_OWNER").val('all');
            }
            for (var i=0;i<data.projectList.length;i++){
                if (data.projectList[i].pk==row.fields.OWNER_PROJECT_ID){
                    $('#UPDATE_OWNER').append('<option value="'+data.projectList[i].pk+'" selected>'+data.projectList[i].fields.NAME+'</option>')
                }else{
                    $('#UPDATE_OWNER').append('<option value="'+data.projectList[i].pk+'" >'+data.projectList[i].fields.NAME+'</option>')
                }
            }
        },
        error: function(data) {
            opt_commons.dialogShow("错误",data.status+":"+data.statusText,2000);
        },
    });
    $('#UPDATE_SYSTEM_ID').html('');
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
                if (data.systemList[i].fields.NAME==row.fields.SYSTEM_ID){
                    $('#UPDATE_SYSTEM_ID').append('<option value="'+data.systemList[i].pk+'" selected>'+data.systemList[i].fields.NAME+'</option>')
                }else{
                    $('#UPDATE_SYSTEM_ID').append('<option value="'+data.systemList[i].pk+'">'+data.systemList[i].fields.NAME+'</option>')
                }

            }

        },
        error: function(data) {
            console.log('error')
        }

    })

}
function updateHost(){
    opt_commons.query_validate("#update_host_form");
    //校验不成功
    if (!$('#update_host_form').valid()){
        return;
    }

    $.ajax({
       url:"/app_cmdb/host/update",
       type:"POST",
       data:{
           id:$("#updateHost_id").val(),
           SYSTEM_ID:$("#UPDATE_SYSTEM_ID").val(),
           NAME:$("#UPDATE_NAME").val(),
           DESCRIPTION:$("#UPDATE_DESCRIPTION").val(),
           OWNER:$("#UPDATE_OWNER").val(),
           MACHINE_TYPE:$("#UPDATE_MACHINE_TYPE").val(),
           MACHINE_ROOM:$("#UPDATE_MACHINE_ROOM").val(),
           MACHINE_POSITION:$("#UPDATE_MACHINE_POSITION").val(),
           CUTTER_NUMBER:$("#UPDATE_CUTTER_NUMBER").val(),
           SN_NUMBER:$("#UPDATE_SN_NUMBER").val(),
           OS:$("#UPDATE_OS").val(),
           NOTE:$("#UPDATE_NOTE").val(),
           PHYSICAL_MACHINE_TYPE:$("#UPDATE_PHYSICAL_MACHINE_TYPE").val(),
           VARIABLES:$("#UPDATE_VARIABLES").val() ? $('#UPDATE_VARIABLES').val():"",
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
               $("#host_table").bootstrapTable('refresh');
                return;
           }
       },
        error: function(data) {
            opt_commons.dialogShow("错误",data.status+":"+data.statusText,2000);

        },
   });

}
  function search() {
    $("#host_table").bootstrapTable('refresh');
  }

  function searchReset(){
       $("#name").val("");
       $("#description").val("");
      $("#system").val("0");
       search();
   }



function exportHost(){
    $.ajax({
        type: 'POST',
        url: "/app_cmdb/host/export",
        data:{
            name:$("#name").val(),
            description:$("#description").val(),
            systemId:$("#system").val(),

        },
        dataType: "json",
        success: function (data) {
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
                downloadExcel(data.filepath);
            }
        },
        error: function () {
            opt_commons.dialogShow("错误","error",2000);
        },
        complete: function () {
            console.log("complete");
        }
    })
    $("#exportModal").modal('hide');

}

function downloadExcel(filepath){
    window.open("/app_cmdb/host/export/download?filepath="+filepath);
    // window.open("/app_tower/group/export/download?filepath="+filepath+'&filename='+filename);
}



//@ sourceURL=host.js