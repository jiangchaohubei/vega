/**
 * Created by PC on 2018/1/11.
 */

$(function () {
    //textarea全屏
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
    var input={
        name:name,
        des:des,
        type:type,
        def:def,
        isrequired:isrequired
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
    $('#updateInputParamModal').modal('show')
    $('#update_input_id').val(id)
    $('#update_input_name').val(INPUTPARAM[parseInt(id)].name)
    $('#update_input_des').val(INPUTPARAM[parseInt(id)].des)
    $('#update_input_type').val(INPUTPARAM[parseInt(id)].type)
    $('#update_input_default').val(INPUTPARAM[parseInt(id)].def)
    $('#update_input_isrequired').prop("checked", INPUTPARAM[parseInt(id)].isrequired);

}
function updateInputParam() {
    var id=$('#update_input_id').val()
    var name=$('#update_input_name').val()
    var des=$('#update_input_des').val()
    var type=$('#update_input_type').val()
    var def=$('#update_input_default').val()
    var isrequired=$('#update_input_isrequired').is(":checked")
    var input={
        name:name,
        des:des,
        type:type,
        def:def,
        isrequired:isrequired
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



//@ sourceURL=createTool.js