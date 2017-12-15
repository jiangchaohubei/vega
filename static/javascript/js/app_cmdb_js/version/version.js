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
function  onload_version() {
    var C1=window.location.href.split("?")[1];
    var id=C1.split("&")[0].split('=')[1];
    var name=decodeURI(C1.split("&")[1].split('=')[1]);
    $('#softwareName').html(name);
    $('#softwareId').val(id);
    $('#toCreateVersion').prop("href", "/static/templates/pages/app_cmdb_pages/version/version_create.html?id="+id+"&name="+name);
    var oTable_inventories = new TableInit_inventories();
    oTable_inventories.Init();

}

var TableInit_inventories = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
       $('#version_table').bootstrapTable({
            url: '/app_cmdb/version/select',

            method:"GET",
            striped: true, //是否显示行间隔色
            cache: false, //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true, //是否显示分页（*）
            sortable: true, //是否启用排序
            sortOrder: "desc",
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
                title: '版本号',
                align : 'center',
                sortable : true,
                // formatter:function(value, row, index){
                //     return '<a href="/static/templates/pages/app_cmdb_pages/package/package.html?id='+row.pk+'&name='+value+'">'+row.fields.NAME+'</a>'
                //
                //  }

            },{
                field: 'fields.DESCRIPTION',
                title: '描述',
                align : 'center',
                sortable : true

            },{
                    field: 'fields.ARGS1',
                    title: '所属程序',
                    align : 'center',
                    sortable : true

                }, {
                    field: 'fields.PACKAGE_PATH',
                    title: '存储路径',
                    align : 'center',
                    sortable : true

                },{
                //field: 'count',
                title: '操作',
                align : 'center',
                sortable : true,
                formatter:function(value, row, index){
                    var data=JSON.stringify(row);
                        return "    <a  class='btn btn-danger btn-xs' title=" + '删除' +
            " href='javascript:showDeleteVersionModal(" + data +");'>" +
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
            softwareId:$("#softwareId").val(),
        };
        return temp;
    };


return oTableInit;
};


 //删除主机组模态框
 function showDeleteVersionModal(row){
     $('#deleteVersionModal').modal('show');
     $('#delete_id').val(row.pk);
     $('#DELETE_NAME').html(row.fields.NAME);
     $('#DELETE_DESCRIPTION').html(row.fields.DESCRIPTION);
     $('#DELETE_SOFTWARE_ID').html(row.fields.ARGS1);

     $('#DELETE_PACKAGE_PATH').html(row.fields.PACKAGE_PATH);
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
function deleteVersion(){
    var id=$("#delete_id").val();
     $.ajax({
       url:"/app_cmdb/version/delete",
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
               $("#version_table").bootstrapTable('refresh');
               return;
           }
           if(data.resultCode=="0001"){
               opt_commons.dialogShow("失败信息","删除失败，禁止删除！",2000);
               $("#version_table").bootstrapTable('refresh');
               return;
           }
       },
       error: function(data) {
              opt_commons.dialogShow("错误",data.status+":"+data.statusText,2000);

        },
   });
}

 //修改主机组模态框
function updateVersionModal(row){
    $('#updateVersionModal').modal('show');
    $('#updateVersion_id').val(row.pk);
    $('#UPDATE_NAME').val(row.fields.NAME);
    $('#UPDATE_DESCRIPTION').val(row.fields.DESCRIPTION);
    $('#UPDATE_RESPONSIBLE_PERSON').val(row.fields.RESPONSIBLE_PERSON);
    $('#UPDATE_LISTEN_PORT').val(row.fields.LISTEN_PORT);
    $('#UPDATE_DEPLOY_DIR').val(row.fields.DEPLOY_DIR);
    $('#UPDATE_DEPLOY_ACCOUNT').val(row.fields.DEPLOY_ACCOUNT);
    $('#UPDATE_TIMER_SCRIPT').val(row.fields.TIMER_SCRIPT);
    $('#UPDATE_LOG_EXPORT').val(row.fields.LOG_EXPORT);
    $('#UPDATE_NOTE').val(row.fields.NOTE);
    $('#UPDATE_DATA_BACKUPPATH').val(row.fields.DATA_BACKUPPATH);
    $('#UPDATE_DATA_FILEPATH').val(row.fields.DATA_FILEPATH);
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
    $('#UPDATE_MODULE_ID').html('');
    $.ajax({
        url:"/app_cmdb/module/init_module_select",
        type:"POST",
        data:{

        },
        dataType:"json",
        success:function(data){
            if (data.resultCode=="0087"){
                alert(data.resultDesc);
                top.location.href ='/login'
            }
            for (var i=0;i<data.moduleList.length;i++){
                if (data.moduleList[i].fields.NAME==row.fields.MODULE_ID){
                    $('#UPDATE_MODULE_ID').append('<option value="'+data.moduleList[i].pk+'" selected>'+data.moduleList[i].fields.NAME+'</option>')
                }else{
                    $('#UPDATE_MODULE_ID').append('<option value="'+data.moduleList[i].pk+'">'+data.moduleList[i].fields.NAME+'</option>')
                }

            }

        },
        error: function(data) {
            console.log('error')
        }

    })

}
function updateVersion(){
    opt_commons.query_validate("#update_version_form");
    //校验不成功
    if (!$('#update_version_form').valid()){
        return;
    }

    $.ajax({
       url:"/app_cmdb/version/update",
       type:"POST",
       data:{
           id:$("#updateVersion_id").val(),
           NAME:$("#UPDATE_NAME").val(),
           DESCRIPTION:$("#UPDATE_DESCRIPTION").val(),
           SYSTEM_ID:$("#UPDATE_SYSTEM_ID").val(),
           RESPONSIBLE_PERSON:$("#UPDATE_RESPONSIBLE_PERSON").val(),
           OWNER:$("#UPDATE_OWNER").val(),
           LISTEN_PORT:$("#UPDATE_LISTEN_PORT").val(),
           DEPLOY_DIR:$("#UPDATE_DEPLOY_DIR").val(),
           DEPLOY_ACCOUNT:$("#UPDATE_DEPLOY_ACCOUNT").val(),
           TIMER_SCRIPT:$("#UPDATE_TIMER_SCRIPT").val(),
           LOG_EXPORT:$("#UPDATE_LOG_EXPORT").val(),
           NOTE:$("#UPDATE_NOTE").val(),
           DATA_BACKUPPATH:$("#UPDATE_DATA_BACKUPPATH").val(),
           DATA_FILEPATH:$("#UPDATE_DATA_FILEPATH").val(),
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
               $("#version_table").bootstrapTable('refresh');
                return;
           }
       },
        error: function(data) {
            opt_commons.dialogShow("错误",data.status+":"+data.statusText,2000);

        },
   });

}
  function search() {
    $("#version_table").bootstrapTable('refresh');
  }

  function searchReset(){
       $("#name").val("");
       $("#description").val("");
       search();
   }






//@ sourceURL=version.js