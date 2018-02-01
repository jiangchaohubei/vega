/**
 * Created by PC on 2018/1/19.
 */

var selectionIds = [];  //����ѡ��ids
Array.prototype.removeByValue = function(val) {
    for(var i=0; i<this.length; i++) {
        if(this[i] == val) {
            this.splice(i, 1);
            break;
        }
    }
}
$(function(){
    var oTable_message = new TableInit_message();
    oTable_message.Init();


})

var TableInit_message = function () {
    var oTableInit = new Object();
    //��ʼ��Table
    oTableInit.Init = function () {
        $('#message_table').bootstrapTable({
            url: '/app_tower/message/select',

            method:"GET",
            striped: true, //�Ƿ���ʾ�м��ɫ
            cache: false, //�Ƿ�ʹ�û��棬Ĭ��Ϊtrue������һ���������Ҫ����һ��������ԣ�*��
            pagination: true, //�Ƿ���ʾ��ҳ��*��
            sortable: true, //�Ƿ���������
            sortOrder: "asc",
            queryParams: oTableInit.queryParams,//���ݲ�����*��
            sidePagination: "server", //��ҳ��ʽ��client�ͻ��˷�ҳ��server����˷�ҳ��*��
            pageNumber:1, //��ʼ�����ص�һҳ��Ĭ�ϵ�һҳ
            pageSize: 5, //ÿҳ�ļ�¼������*��
            pageList: [5, 20, 50, 100], //�ɹ�ѡ���ÿҳ��������*��
            strictSearch: true,
            showColumns: true, //�Ƿ���ʾ���е���
            showRefresh: true, //�Ƿ���ʾˢ�°�ť
            minimumCountColumns: 2, //�������������
            clickToSelect: false, //�Ƿ����õ��ѡ����
            height: 345, //�иߣ����û������height���ԣ�����Զ����ݼ�¼�������ñ��߶�
            showToggle:true, //�Ƿ���ʾ��ϸ��ͼ���б���ͼ���л���ť
            cardView: false, //�Ƿ���ʾ��ϸ��ͼ
            detailView: false, //�Ƿ���ʾ���ӱ�
            onCheck: function (row) {
                //������ǰ���checkbox��ѡ��
                console.log(row)
                if ($.inArray(row.pk, selectionIds)== -1){//������
                    selectionIds.push(row.pk);
                }
            },
            onUncheck: function (row) {
                //������ǰ���checkbox��ȡ��
                console.log(row)
                if ($.inArray(row.pk, selectionIds)!= -1){//����
                    selectionIds.removeByValue(row.pk)
                }


            },
            onCheckAll: function (rows) {
                //��ϵ�checkbox��ѡ��
                console.log(rows)
                for (var i=0;i<rows.length;i++){
                    if ($.inArray(rows[i].pk, selectionIds)== -1){//������
                        selectionIds.push(rows[i].pk)
                    }
                }
            },
            onUncheckAll: function (rows) {
                //��ϵ�checkbox��ȡ��
                console.log(rows)
                for (var i=0;i<rows.length;i++){
                    if ($.inArray(rows[i].pk, selectionIds)!= -1){//����
                        selectionIds.removeByValue(rows[i].pk)
                    }
                }
            },
            responseHandler: function(res) { //�������ݴ���
                if (res.resultCode=="0087"){
                    alert(res.resultDesc);
                    top.location.href ='/login'
                }
                if(res.resultCode=="0057"){
                    $('.fixed-table-loading').html(res.resultDesc)
                    return;
                }
                if(res.resultCode=="0001"){
                    opt_commons.dialogShow("��ʾ��Ϣ",res.resultDesc,2000);
                    return;
                }
                var data=JSON.parse(res.rows);
                $.each(data, function (i, row) {
                    row.checkStatus = $.inArray(row.pk, selectionIds) != -1;  //�жϵ�ǰ�е�����id�Ƿ������ѡ�е����飬�����򽫶�ѡ��״̬��Ϊtrue
                });
                return {
                    "total": res.total,//��ҳ��
                    "rows": data  //����
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
                    field: 'fields.CONTENT',
                    title: '��Ϣ����',
                    align : 'center',
                    sortable : true,


                },{
                    field: 'fields.TYPE',
                    title: '��Ϣ����',
                    align : 'center',
                    sortable : true,


                },{
                    field: 'fields.CREATE_TIME',
                    title: 'ʱ��',
                    align : 'center',
                    sortable : true

                }, ]
        });
    };

    //�õ���ѯ�Ĳ���
    oTableInit.queryParams = function (params) {
        var temp = { //����ļ������ֺͿ������ı���������һֱ����߸Ķ���������Ҳ��Ҫ�ĳ�һ����
            limit: params.limit, //ҳ���С
            offset: params.offset, //ҳ��
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
    $("#message_table").bootstrapTable('refresh');
}



//@ sourceURL=message.js