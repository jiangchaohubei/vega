/**
 * Created by PC on 2018/1/11.
 */

$(function () {
    //textarea全屏,图标插件
    $('#tool_scriptCode').textareafullscreen();

    $.ajax({
        url:"/app_tower/workingPlatform/toolcreate_init",
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
            if(data.resultCode=="0001"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            if(data.resultCode=="0000"){
                for (var i=0;i<data.tooltypeList.length;i++){
                    $('#tool_type_select').append('<option value="'+data.tooltypeList[i].fields.NAME+'">'+data.tooltypeList[i].fields.NAME+'</option>')
                }
                for (var i=0;i<data.projectList.length;i++){
                    $('#tool_owner').append('<option value="'+data.projectList[i].pk+'">'+data.projectList[i].fields.NAME+'</option>')
                }
                var newIcons=[]
                for (var i=0;i<data.imgList.length;i++){
                    newIcons.push(data.imgList[i].fields.NAME);
                }
                $('#tool_icon').iconPicker({newIcons:newIcons});

                return;
            }
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error",2000);


        },
    });
})

var INPUTPARAM=[]
function addInputParam() {
    var name=$('#add_input_name').val()
    var des=$('#add_input_des').val()
    var type=$('#add_input_type').val()
    var def=$('#add_input_default').val()
    var isrequired=$('#add_input_isrequired').is(":checked")
    var enums=[]
    if (type==3){
        $('#enumInputList input').forEach(function (v,n) {
            var enumInput=$(v).val()
            if (enumInput){
                enums.push(enumInput)
            }
        })
    }
    
    var input={
        name:name,
        des:des,
        type:type,
        def:def,
        isrequired:isrequired,
        enums:enums
    }
    var id=INPUTPARAM.push(input)-1
    var inputid="input"+id
    $('#inputList').append(
        '<div class="inputItem" id="'+inputid+'" onclick="showInputModal('+id+')">'+
            '<label for="inventory" class="control-label col-md-2  requiredField" style="height:64px;line-height:50px;text-align:center">'+name+':</label>'+
             '<div class="controls col-md-10" style="height:64px;">'+
                 ' <input type="text" class="form-control" value="'+def+'" placeholder="'+des+'" >'+
             '</div>'+
         '</div>'
    )

}

function showInputModal(id) {

    $('#update_input_id').val(id)
    $('#update_input_name').val(INPUTPARAM[parseInt(id)].name)
    $('#update_input_des').val(INPUTPARAM[parseInt(id)].des)
    $('#update_input_type').val(INPUTPARAM[parseInt(id)].type).change()
    $('#update_input_default').val(INPUTPARAM[parseInt(id)].def)
    $('#update_input_isrequired').prop("checked", INPUTPARAM[parseInt(id)].isrequired);
    $('#enumInputList').html('')
    var enums=INPUTPARAM[parseInt(id)].enums
    if(enums){
        for (var i=0;i<enums.length;i++){
            $('#enumInputList').append('<input type="text" value="'+enums[i]+'"  class="form-control">')
        }
    }

    $('#updateInputParamModal').modal('show')

}
function updateInputParam() {
    var id=$('#update_input_id').val()
    var name=$('#update_input_name').val()
    var des=$('#update_input_des').val()
    var type=$('#update_input_type').val()
    var def=$('#update_input_default').val()
    var isrequired=$('#update_input_isrequired').is(":checked")
    var enums=[]
    if (type==3){
        $('#enumInputList input').forEach(function (v,n) {
            var enumInput=$(v).val()
            if (enumInput){
                enums.push(enumInput)
            }
        })
    }
    var input={
        name:name,
        des:des,
        type:type,
        def:def,
        isrequired:isrequired,
        enums:enums
    }
    INPUTPARAM[parseInt(id)]=input
    var inputid="input"+id
    $('#'+inputid).html('')
    $('#'+inputid).append(
        '<label for="inventory" class="control-label col-md-2  requiredField" style="height:64px;line-height:50px;text-align:center">'+name+':</label>'+
        '<div class="controls col-md-10" style="height:64px;">'+
        ' <input type="text" class="form-control" value="'+def+'" placeholder="'+des+'" >'+
        '</div>'
    )
}
function deleteInputParam() {
    var id=$('#update_input_id').val()
    INPUTPARAM[parseInt(id)]=0
    var inputid="input"+id
    $('#'+inputid).html('')
}


var OUTPUTPARAM=[]
function addOutputParam() {
    var name=$('#add_output_name').val()
    var des=$('#add_output_des').val()
    var type=$('#add_output_type').val()

    var output={
        name:name,
        des:des,
        type:type,
    }
    var id=OUTPUTPARAM.push(output)-1
    var outputid="output"+id
    $('#outputTbody').append(
                '<tr id="'+outputid+'" onclick="showOutputModal('+id+')">'+
                    '<td>'+id+'</td>'+
                    '<td>'+name+'</td>'+
                    '<td>'+des+'</td>'+
                    '<td>'+type+'</td>'+
                '</tr>'

    )

}

function showOutputModal(id) {
    $('#updateOutputParamModal').modal('show')
    $('#update_output_id').val(id)
    $('#update_output_name').val(OUTPUTPARAM[parseInt(id)].name)
    $('#update_output_des').val(OUTPUTPARAM[parseInt(id)].des)
    $('#update_output_type').val(OUTPUTPARAM[parseInt(id)].type)
}
function updateOutputParam() {
    var id=$('#update_output_id').val()
    var name=$('#update_output_name').val()
    var des=$('#update_output_des').val()
    var type=$('#update_output_type').val()

    var output={
        name:name,
        des:des,
        type:type,

    }
    OUTPUTPARAM[parseInt(id)]=output
    var outputid="output"+id
    $('#'+outputid).html('')
    $('#'+outputid).append(
        '<td>'+id+'</td>'+
        '<td>'+name+'</td>'+
        '<td>'+des+'</td>'+
        '<td>'+type+'</td>'
    )
}
function deleteOutputParam() {
    var id=$('#update_output_id').val()
    OUTPUTPARAM[parseInt(id)]=0
    var outputid="output"+id
    $('#'+outputid).html('')
}


function addTool() {
    var name=$('#tool_name').val();
    var type=$('#tool_type').val();
    var icon=$('#tool_icon').val();
    var dangerlevel=$("#tool_dangerlevel input[name='tool-radio']:checked").val();
    var language=$('#tool_language').find('.span-chooice-click').html()
    var scriptCode=$('#tool_scriptCode').val();
    var des=$('#tool_des').val();
    var inputParam=INPUTPARAM;
    var outputParam=OUTPUTPARAM;
    var owner=$('#tool_owner').val()
    $.ajax({
        url:"/app_tower/workingPlatform/tool_add",
        type:"POST",
        data:{
            name:name,
            type:type,
            icon:icon,
            dangerlevel:dangerlevel,
            language:language,
            scriptCode:scriptCode,
            des:des,
            inputParam:JSON.stringify(inputParam),
            outputParam:JSON.stringify(outputParam),
            owner:owner,
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
                window.location.href='/static/templates/pages/app_tower_pages/workingPlatform/working.html'
                return;
            }
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error",2000);


        },
    });


}

function showImgUploadModal() {
    //指定上传controller访问地址
    var path = '/app_tower/workingPlatform/icon_upload';
    //页面初始化加载
    var oFileInput = new FileInput();
    oFileInput.Init("itemImagers", path);

    $('#imgUploadModal').modal('show');
}

//初始化fileinput
var FileInput = function () {
    var oFile = new Object();
//初始化fileinput控件（第一次初始化）
    oFile.Init = function(ctrlName, uploadUrl) {
        var control = $('#' + ctrlName);
        //初始化上传控件的样式
        control.fileinput({
            language: 'zh', //设置语言
            uploadUrl: uploadUrl, //上传的地址
            allowedFileExtensions : ['jpg', 'png','bmp','jpeg'],//接收的文件后缀
            showUpload: true, //是否显示上传按钮
            autoReplace: true,
            browseClass: "btn btn-primary", //按钮样式
            maxFileCount: 10, //表示允许同时上传的最大文件个数
            enctype: 'multipart/form-data',
            validateInitialCount:true,
            previewFileIcon: "<i class='glyphicon glyphicon-king'></i>",
            msgFilesTooMany: "选择上传的文件数量({n}) 超过允许的最大数值{m}！",
        })
        .on("fileuploaded", function (event, data, previewId, index) {
            if (data.response.resultCode=="0087"){
                alert(data.response.resultDesc);
                top.location.href ='/login'
            }
            if(data.response.resultCode=="0057"){
                opt_commons.dialogShow("提示信息",data.response.resultDesc,2000);
                return;
            }
            if(data.response.resultCode=="0001"){
                opt_commons.dialogShow("提示信息",data.response.resultDesc,2000);
                return;
            }
            if(data.response.resultCode=="0000"){
                opt_commons.dialogShow("成功信息","添加成功！",2000);
                iconPickerFresh();
                return;
            }

        });


    }
    return oFile;
};
//刷新图标选择
function iconPickerFresh() {
    $.ajax({
        url:"/app_tower/workingPlatform/icons_init",
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
            if(data.resultCode=="0001"){
                opt_commons.dialogShow("提示信息",data.resultDesc,2000);
                return;
            }
            if(data.resultCode=="0000"){

                var newIcons=[]
                for (var i=0;i<data.imgList.length;i++){
                    newIcons.push(data.imgList[i].fields.NAME);
                }
                $('#tool_icon').iconPicker({newIcons:newIcons,refresh:true});

                return;
            }
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error",2000);


        },
    });
}

//增加枚举文本框
function addEnumInput() {
    $('#enumInputList').append('<input type="text"  class="form-control">')
}

function showAddInputParamModal() {
    $('#add_input_name').val('')
    $('#add_input_des').val('')
    $('#add_input_type').val(0).change()
    $('#add_input_default').val('')
    $('#add_input_isrequired').prop("checked", false);
    $('#enumInputList').html('')
    $('#addInputParamModal').modal('show')
}
//@ sourceURL=createTool.js