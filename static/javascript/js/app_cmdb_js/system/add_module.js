/**
 * Created by PC on 2017/8/17.
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
function  onload_module() {
    var C1=window.location.href.split("?")[1];
    var id=C1.split("&")[0].split('=')[1];
    var name=decodeURI(C1.split("&")[1].split('=')[1]);
    $('#systemName').html(name);
    $('#systemId').val(id);
    $('#MODULE_SYSTEM_ID_1').html(name)
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

    var oTable_inventories = new TableInit_inventories();
    oTable_inventories.Init();
}
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
            SYSTEM_ID:$('#systemId').val(),


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
                $("#module_table").bootstrapTable('refresh');
                return;
            }
        },
        error: function(data) {
            console.log(data)
                opt_commons.dialogShow("错误",data.status+":"+data.statusText,2000);
        },
    })

}

var TableInit_inventories = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#module_table').bootstrapTable({
            url: '/app_cmdb/module/select',

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
                    title: '模块名称',
                    align : 'center',
                    sortable : true,


                },{
                    field: 'fields.DESCRIPTION',
                    title: '描述',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.SYSTEM_ID',
                    title: '所属系统',
                    align : 'center',
                    sortable : true

                }, {
                    field: 'fields.RESPONSIBLE_PERSON',
                    title: '责任人',
                    align : 'center',
                    sortable : true

                },{
                    //field: 'count',
                    title: '操作',
                    align : 'center',
                    sortable : true,
                    formatter:function(value, row, index){
                        var data=JSON.stringify(row);
                        return "<a class='btn btn-warning btn-xs' title=" + '编辑' +
                            " href='javascript:updateModuleModal(" + data + ");'>" +
                            "<i class='ace-icon fa fa-pencil bigger-130'></i>编辑</a>" +
                            "    <a  class='btn btn-danger btn-xs' title=" + '删除' +
                            " href='javascript:showDeleteModuleModal(" + data +");'>" +
                            "<i class='ace-icon fa fa-trash-o bigger-130'></i>删除</a>";
                            // "    <a  class='btn btn-danger btn-xs' title=" + '添加程序' +
                            // " href='javascript:addSoftware(" + data +");'>" +
                            // "<i class='ace-icon fa fa-plus bigger-130'></i>添加程序</a>"
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
            name:"",
            description:"",
            systemId:$('#systemId').val()
        };
        return temp;
    };


    return oTableInit;
};
function addSoftware(row) {
    window.location.href="/static/templates/pages/app_cmdb_pages/module/software_add.html?id="+row.pk+"&name="+row.fields.NAME
}

//删除模块模态框
function showDeleteModuleModal(row){
    $('#deleteModuleModal').modal('show');
    $('#delete_id').val(row.pk);
    $('#DELETE_NAME').html(row.fields.NAME);
    $('#DELETE_DESCRIPTION').html(row.fields.DESCRIPTION);
    $('#DELETE_SYSTEM_ID').html(row.fields.SYSTEM_ID);
    $('#DELETE_RESPONSIBLE_PERSON').html(row.fields.RESPONSIBLE_PERSON);
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
function deleteModule(){
    var id=$("#delete_id").val();
    $.ajax({
        url:"/app_cmdb/module/delete",
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
                opt_commons.dialogShow("成功信息","删除成功！",2000);
                $("#module_table").bootstrapTable('refresh');
                return;
            }
            if(data.resultCode=="0001"){
                opt_commons.dialogShow("失败信息","删除失败，禁止删除！",2000);
                $("#module_table").bootstrapTable('refresh');
                return;
            }
        },
        error: function(data) {
            opt_commons.dialogShow("错误",data.status+":"+data.statusText,2000);

        },
    });
}

//修改主机组模态框
function updateModuleModal(row){
    $('#updateModuleModal').modal('show');
    $('#updateModule_id').val(row.pk);
    $('#UPDATE_NAME').val(row.fields.NAME);
    $('#UPDATE_DESCRIPTION').val(row.fields.DESCRIPTION);

    $('#UPDATE_RESPONSIBLE_PERSON').val(row.fields.RESPONSIBLE_PERSON);
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
function updateModule(){
    opt_commons.query_validate("#update_module_form");
    //校验不成功
    if (!$('#update_module_form').valid()){
        return;
    }

    $.ajax({
        url:"/app_cmdb/module/update",
        type:"POST",
        data:{
            id:$("#updateModule_id").val(),
            NAME:$("#UPDATE_NAME").val(),
            DESCRIPTION:$("#UPDATE_DESCRIPTION").val(),
            SYSTEM_ID:$("#UPDATE_SYSTEM_ID").val(),
            RESPONSIBLE_PERSON:$("#UPDATE_RESPONSIBLE_PERSON").val(),
            OWNER:$("#UPDATE_OWNER").val()
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
                $("#module_table").bootstrapTable('refresh');
                return;
            }
        },
        error: function(data) {
            opt_commons.dialogShow("错误",data.status+":"+data.statusText,2000);

        },
    });

}




//@ sourceURL=add_module.js