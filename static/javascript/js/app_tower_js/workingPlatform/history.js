/**
 * Created by PC on 2018/1/19.
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
    var oTable_toolHistory = new TableInit_toolHistory();
    oTable_toolHistory.Init();


})

var TableInit_toolHistory = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#toolHistory_table').bootstrapTable({
            url: '/app_tower/workingPlatform/history_select',

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
                    field: 'fields.ARGS1',
                    title: '任务工具',
                    align : 'center',
                    sortable : true,
                    formatter:function(value, row, index){
                        return  '<a href="/static/templates/pages/app_tower_pages/workingPlatform/historyDetail.html?id='+row.pk+'&name='+row.fields.ARGS1+'">'+value+'</a>'

                    }

                },{
                    field: 'fields.ARGS2',
                    title: '描述',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.STATUS',
                    title: '状态',
                    align : 'center',
                    sortable : true,
                    formatter:function(value, row, index){
                        if (value=='SUCCESS'){
                            return '<span class="label label-success">'+'成功'+'</span>'
                        }else if (value=='FAILURE'){
                            return '<span class="label label-danger">'+'失败'+'</span>'
                        }else if (value=='STARTED'){
                            return '<span class="label label-info">'+'执行中'+'</span>'
                        }else if (value=='REVOKED') {
                            return '<span class="label label-default">' + '取消' + '</span>'
                        }

                    }

                },{
                    field: 'fields.CREATE_USER_NAME',
                    title: '创建者',
                    align : 'center',
                    sortable : true

                },{
                    field: 'fields.CREATE_TIME',
                    title: '开始时间',
                    align : 'center',
                    sortable : true

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
            timeArea:$('#time_area').val()
            // name:$("#name").val().trim(),
            // description:$("#description").val().trim(),
        };
        return temp;
    };
    return oTableInit;
};

function onSelectTime(obj,area) {
    $('#timeArea').find('span').each(function(n,v){
        $(v).removeClass()
        $(v).addClass('span-chooice')
    })
    $(obj).removeClass()
    $(obj).addClass('span-chooice-click')
    $('#time_area').val(area)
    $("#toolHistory_table").bootstrapTable('refresh');
}



//@ sourceURL=history.js