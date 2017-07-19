/**
 * Created by PC on 2017/7/14.
 */
$(function(){
    var oTable_inventories = new TableInit_inventories();
    oTable_inventories.Init();

})

var TableInit_inventories = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#inventories_table').bootstrapTable({
            url: '/app_tower/inventories/select',

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
            clickToSelect: true, //是否启用点击选中行
            height: 345, //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            showToggle:true, //是否显示详细视图和列表视图的切换按钮
            cardView: false, //是否显示详细视图
            detailView: false, //是否显示父子表
            responseHandler: function(res) { //返回数据处理
                console.log(res.rows);
                console.log(JSON.parse(res.rows) )
                return {
                    "total": res.total,//总页数
                    "rows": JSON.parse(res.rows)  //数据
                 };
            },
            columns: [{
                field: 'fields.name',
                title: '清单名称',
                align : 'center',
                sortable : true,
                formatter:function(value, row, index){
                    return '<a href="/static/templates/pages/inventories_name.html">'+value+'</a>'
                }

            },{
                field: 'fields.description',
                title: '公司',
                align : 'center',
                sortable : true

            }, {
                //field: 'count',
                title: '操作',
                align : 'center',
                sortable : true,
                formatter:function(value, row, index){
                        return "<a class='green' title=" + '执行' +
            " href='javascript:showAddScoreModal(\"" + 1 + "\");'>" +
            "<i class='ace-icon fa fa-check bigger-130'></i></a>" +
            "    <a class='blue' title=" + '编辑' +
            " href='javascript:showUpdateScoreRecordModal(\"" + 1 + "\");'>" +
            "<i class='ace-icon fa fa-pencil bigger-130'></i></a>" +
            "    <a class='red' title=" + '删除' +
            " href='javascript:showDeleteScoreModal(\"" + 1 + "\");'>" +
            "<i class='ace-icon fa fa-trash-o bigger-130'></i></a>";
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

            // mealTimeStart:$("#mealTimeStart_meals").val(),
            // mealTimeEnd:$("#mealTimeEnd_meals").val(),
        };
        return temp;
    };
    return oTableInit;
};