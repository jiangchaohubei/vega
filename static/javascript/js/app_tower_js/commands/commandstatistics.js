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
    var oTable_commands = new TableInit_commands_table();
    oTable_commands.Init();

})

var TableInit_commands_table = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
       $('#commands_table').bootstrapTable({
            url: '/app_tower/job/sudo_select',

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
                    $('.fixed-table-loading').html('你没有查看权限！')
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
                visible: true   //可见
            },
                {
                field: 'fields.IP',
                title: 'IP地址',
                align : 'center',
                sortable : true,


            },{
                    field: 'fields.PORT',
                    title: '端口号',
                    align : 'center',
                    sortable : true,


                },{
                    field: 'fields.CREDENTIALS_ID',
                    title: '登录凭证',
                    align : 'center',
                    sortable : true

                },{
                field: 'fields.ACCOUNT',
                title: '账号',
                align : 'center',
                sortable : true

            },{
                    field: 'fields.CREATE_USER_NAME',
                    title: '授权人',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.DESCRIPTION',
                    title: '说明',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.CREATE_TIME',
                    title: '授权时间',
                    align : 'center',
                    sortable : true

                },{
                    title: '操作',
                    align : 'center',
                    sortable : true,
                    formatter:function(value, row, index){
                        var data=JSON.stringify(row)
                        if (row.fields.CREDENTIALS_ID==null){
                            return "<a  class='btn btn-danger btn-xs' title=" + '删除记录' +
                                " href='javascript:showDeleteRecordModal(" + data +");'>" +
                                "<i class='ace-icon fa fa-trash-o bigger-130'></i>删除记录</a>";
                        }else{
                            return "<a  class='btn btn-danger btn-xs' title=" + '回收权限' +
                                " href='javascript:showCallbackModal(" + data +");'>" +
                                "<i class='ace-icon fa fa-trash-o bigger-130'></i>回收权限</a>";
                        }

                    }
                },  ]
        });

       $('.fixed-table-toolbar').append(
          '<div class="columns columns-left btn-group pull-left" style="margin-left: 10px">'+

           ' <div class="keep-open btn-group " title="列">'+

          ' <button type="button"  class="btn btn-info " data-toggle="modal" data-target="#addSudoModal"  >'+
          '  <span class="glyphicon orange2 bigger-115 glyphicon-plus-sign" aria-hidden="true"></span>&nbsp添加'+
          ' </button>'+
        //    ' <button type="button"  class="btn btn-default dropdown-toggle" data-toggle="dropdown" >'+
        //   ' 增加 <span class="caret"></span>'+
        // ' </button>'+
        // ' <ul class="dropdown-menu" style="width: 400px" role="menu">'+
        // '<li ><div class="row col-md-12" style="margin-top:20px"><div class="col-md-5"><label class="">IP地址：</label></div><div class="col-md-7"><input class="form-control " id="addIP" type="text"   placeholder="IP地址"></div></div></li>'+
        // '<li ><div class="row col-md-12" style="margin-top:5px"><div class="col-md-5"><label class="">端口号：</label></div><div class="col-md-7"><input class="form-control " id="addPort" type="text"  placeholder="端口号"></div></div></li>'+
        // '<li ><div class="row col-md-12" style="margin-top:5px"><div class="col-md-5"><label class="">账  号：</label></div><div class="col-md-7"><input class="form-control " id="addAccount" type="text"  placeholder="账  号"></div></div></li>'+
        // '<li ><div class="row col-md-12" style="margin-top:5px"><div class="col-md-5"><label class="">说  明：</label></div><div class="col-md-7"><input class="form-control " id="addDesc" type="text"  placeholder="说  明"></div></div></li>'+
        // ' <li   ><div class="row col-md-12" style="margin-top:10px;margin-bottom: 10px"><button class="form-control btn-success col-md-offset-7" onclick="addSudoRecord()" style="width: 100px">保存</button></div> </li>'+
        //
        // ' </ul>' +
          '</div></div>')
        opt_commons.query_validate("#addSudoForm");
    };

    //得到查询的参数
    oTableInit.queryParams = function (params) {
        var temp = { //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit, //页面大小
            offset: params.offset, //页码
            order: params.order,
            ordername: params.sort,
            ip:$("#search_ip").val().trim(),
            account:$("#search_account").val().trim(),
            createUser:$("#search_createUser").val().trim(),
        };
        return temp;
    };


return oTableInit;
};



  function search() {
    $("#commands_table").bootstrapTable('refresh');
  }

  function searchReset(){
       $("#search_ip").val("");
       $("#search_account").val("");
      $("#search_createUser").val("");

       search();
   }
function showCallbackModal(data) {
    $('#delete_id').val(data.pk)
    $('#callbackModal').modal('show')
}
function  showDeleteRecordModal(data) {
    $('#deleteRecord_id').val(data.pk)
    $('#deleteRecordModal').modal('show')
}
//回收权限
function callbackSudo(){
    var sudoId=$('#delete_id').val();
    var sudoIdList=[]
    sudoIdList.push(sudoId)
    $.ajax({
        type: 'POST',
        url: "/app_tower/job/run_commands_callbackSudoAuth",
        data: {
            sudoIdList: JSON.stringify(sudoIdList),
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
            $("#commands_table").bootstrapTable('refresh');
        },
        error: function () {
            console.log("error");
            opt_commons.dialogShow("提示信息","错误！",2000);
            $("#commands_table").bootstrapTable('refresh');
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })

}
//删除记录
function deleteRecord(){
    var sudoId=$('#deleteRecord_id').val();

    $.ajax({
        type: 'POST',
        url: "/app_tower/job/sudo_delete",
        data: {
            id: sudoId,
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
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                $("#commands_table").bootstrapTable('refresh');
                return;
            }

        },
        error: function () {
            console.log("error");
            opt_commons.dialogShow("提示信息","错误！",2000);
            $("#commands_table").bootstrapTable('refresh');
        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })

}
function addSudoRecord() {
    opt_commons.query_validate("#addSudoForm");
    //校验不成功
    if (!$('#addSudoForm').valid()){
        console.log("校验失败！")
        return;
    }
    var addIP=$('#addSudo_ip').val()
    var addPort=$('#addSudo_port').val()
    var addAccount=$('#addSudo_account').val()
    var addDesc=$('#addSudo_desc').val()
    if (addAccount=='' || addAccount==null || addDesc=='' || addDesc==null){
        opt_commons.dialogShow("提示信息","请填写完整",2000);
        return;
    }
    $.ajax({
        type: 'POST',
        url: "/app_tower/job/sudoRecord_add",
        data: {
            addIP: addIP,
            addPort: addPort,
            addAccount: addAccount,
            addDesc: addDesc,
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
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                $("#commands_table").bootstrapTable('refresh');
                return;
            }

        },
        error: function () {
            console.log("error");
            opt_commons.dialogShow("提示信息","错误！",2000);

        },
        complete: function (XMLHttpRequest, textStatus) {
            console.log("complete");
        }
    })
}



//@ sourceURL=commandstatistics.js