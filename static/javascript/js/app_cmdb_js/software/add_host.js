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
function onload_host_add(){
      opt_commons.query_validate("#host_form");
        C1=window.location.href.split("?")[1];
         id=C1.split("&")[0].split('=')[1];
         name=decodeURI(C1.split("&")[1].split('=')[1]);
        $('#softwareName').html(name);
        $('#softwareId').val(id);
        //$('#uploadGroupId').val(id);
        var oTable_host = new TableInit_host();

        oTable_host.Init();

}
function save_host(){
    //校验不成功
    if (!$('#host_form').valid()){
        return;
    }
    var id=$('#softwareId').val();
    var hoststr=$('#choosed_hosts').val()
    console.log(hoststr)
    var hostList=hoststr.split(',')
    console.log(hostList)
    if (!hostList[hostList.length-1]){
        console.log(hostList)
        hostList.pop()
    }


    $.ajax({
        url:"/app_cmdb/software/host_add",
        type:"POST",
        data:{
            id:id,
            hostList:JSON.stringify(hostList)
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
                var str=""
                if(data.errorHost.length>0){
                    str+="其中主机："+String(data.errorHost)+"不属于当前系统！"
                }
                opt_commons.dialogShow("成功信息","添加成功！"+str);
                $("#host_table").bootstrapTable('refresh');
                $('#choosed_hosts').val('');

                return;
            }
        },
        error: function(data) {

                opt_commons.dialogShow("错误","error",2000);
                console.log("error");

        },
    })

}
var TableInit_host = function () {

    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#host_table').bootstrapTable({
            url: '/app_cmdb/software/host_select',

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
                title: '主机地址',
                align : 'center',
                sortable : true,
                formatter:function(value, row, index){
                    return value
                }

            },{
                field: 'fields.DESCRIPTION',
                title: '描述',
                align : 'center',
                sortable : true

            }, {
                //field: 'count',
                title: '操作',
                align : 'center',
                sortable : true,
                formatter:function(value, row, index){
                    var host=row.pk+","+row.fields.NAME+","+ row.fields.DESCRIPTION+","+row.fields.VARIABLES;
                        return "    <a class='btn btn-danger btn-xs' title=" + '解绑' +
            " href='javascript:showDeleteHostModal(\"" + host + "\");'>" +
            "<i class='ace-icon fa fa-trash-o bigger-130'></i>解绑</a>";
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
            id:$('#softwareId').val(),
        };
        return temp;
    };
    return oTableInit;
};

//删除主机模态框
function showDeleteHostModal(data){
    var host = data.split(',');
    $("#deleteHostModal").modal("show");
    $("#delete_id").val(host[0]);
    $("#deleteName").html(host[1]);
    $("#deleteDescription").html(host[2]);
    $("#deleteVariables").html(host[3]);


}
//解绑主机
function deleteHost(){
    var id=$("#delete_id").val();
    $.ajax({
        url:"/app_cmdb/software/host_delete",
        type:"POST",
        data:{
            id:id,
            softwareId:$('#softwareId').val()
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
                opt_commons.dialogShow("成功信息","解绑成功！",2000);
                $("#host_table").bootstrapTable('refresh');
                return;
            }
        },
        error: function(data) {

                opt_commons.dialogShow("错误","error",2000);
                $("#host_table").bootstrapTable('refresh');

        },
    });
}



//模态框
function showCmdbModal(){

    $("#cmdbModal").modal("show");

    $.ajax({
        url:"/app_cmdb/software/init_cmdb_system",
        type:"POST",
        data:{
                softwareId:$('#softwareId').val()
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

                $('#cmdb_system').html('')
                $('#cmdb_system').append('<option value="'+data.systemId+'" selected>'+data.systemName+'</option>')

                search_cmdb()

            }
            if(data.resultCode=="0001"){
                opt_commons.dialogShow("失败信息",data.resultDesc,2000);

                return;
            }
        },
        error: function(data) {

            opt_commons.dialogShow("失败信息","error",2000);

        },
    });




}

function search_cmdb() {
    $.ajax({
        url:"/app_tower/host/selectBySomething",
        type:"POST",
        data:{
            system_id:$('#cmdb_system').val(),
            keyword:$('#cmdb_keyword').val(),
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

                var str=""
                for (var i=0;i<data.hostList.length;i++){
                    str+='<tr>'+
                        '<td><label class="ui-checkbox"><input type="checkbox"  value="'+data.hostList[i].fields.NAME+'"><span></span></label></td>'+
                        ' <td class="text-may-ellipsis">'+data.hostList[i].pk+'</td>'+
                        ' <td class="text-may-ellipsis">'+data.hostList[i].fields.NAME+'</td>'+
                        '<td class="text-may-ellipsis" style="max-width: 224px;">'+data.hostList[i].fields.DESCRIPTION+'</td>'+
                        '<td class="text-may-ellipsis" style="max-width: 224px;">'+data.hostList[i].fields.MACHINE_TYPE+'</td>'+
                        '<td class="text-may-ellipsis" style="max-width: 224px;">'+data.hostList[i].fields.MACHINE_ROOM+'</td>'+
                        '</tr>'
                }
                $('#cmdb_tbody').html('')
                $('#cmdb_tbody').append(str)

            }
            if(data.resultCode=="0001"){
                opt_commons.dialogShow("失败信息",data.resultDesc,2000);

                return;
            }
        },
        error: function(data) {

            opt_commons.dialogShow("失败信息","error",2000);

        },
    });
}

function beSureChoose() {
    var ips=""
    $('#cmdb_tbody').find('input').each(function (n,v) {
        if ($(v).is(":checked")){
            ips+=$(v).val()+","
        }

    })
    $('#choosed_hosts').val(ips)
}

//@ sourceURL=add_host.js