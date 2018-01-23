/**
 * Created by PC on 2018/1/11.
 */
var INPUTPARAM=[]
var OUTPUTPARAM=[]
function  onload_editTool() {
    var C1 = window.location.href.split("?")[1];
    var C2 = C1.split("&");
    var toolid = C2[0].split("=")[1]
    var toolname = decodeURI(C2[1].split("=")[1])
    $('#toolname').html(toolname)
    $('#toolid').val(toolid)
    $('#toolDetail').attr('href','/static/templates/pages/app_tower_pages/workingPlatform/toolDetail.html?toolid='+toolid+'&toolname='+toolname)
    $('#toolDetail').html(toolname)
    //textarea全屏
    $('#tool_scriptCode').textareafullscreen();
    $.ajax({
        url:"/app_tower/workingPlatform/tooledit_init",
        type:"POST",
        data:{
            toolid:toolid
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
                $('#tool_name').val(data.tool.NAME)
                if (data.tool.SCRIPT_LANGUAGE==0){
                    $('#yaml').removeClass('span-chooice-click')
                    $('#yaml').addClass('span-chooice')
                    $('#shell').removeClass('span-chooice')
                    $('#shell').addClass('span-chooice-click')
                }else if (data.tool.SCRIPT_LANGUAGE==1) {
                    $('#yaml').removeClass('span-chooice-click')
                    $('#yaml').addClass('span-chooice')
                    $('#python').removeClass('span-chooice')
                    $('#python').addClass('span-chooice-click')
                }
                for (var i=0;i<data.tooltypeList.length;i++){
                    if (data.tool.TOOLTYPE_ID==data.tooltypeList[i].pk){
                        $('#tool_type').val(data.tooltypeList[i].fields.NAME)
                    }
                    $('#tool_type_select').append('<option value="'+data.tooltypeList[i].fields.NAME+'">'+data.tooltypeList[i].fields.NAME+'</option>')
                }
                $('#tool_scriptCode').val(data.tool.SCRIPT_CODE)
                $('#tool_des').val(data.tool.DESCRIPTION)
                $("#tool_owner").html('');
                $('#tool_owner').append('<option value="onlyOne" selected>'+'仅自己'+'</option>')
                $('#tool_owner').append('<option value="all" >'+'所有人'+'</option>')
                if (data.tool.OWNER_ID){
                    $("#tool_owner").val('onlyOne');
                }else if(data.tool.OWNER_ALL){
                    $("#tool_owner").val('all');
                }
                for (var i=0;i<data.projectList.length;i++){
                    if (data.projectList[i].pk==data.tool.OWNER_PROJECT_ID){
                        $('#tool_owner').append('<option value="'+data.projectList[i].pk+'" selected>'+data.projectList[i].fields.NAME+'</option>')
                    }else{
                        $('#tool_owner').append('<option value="'+data.projectList[i].pk+'">'+data.projectList[i].fields.NAME+'</option>')

                    }
                }
                for (var i=0;i<data.toolinput.length;i++){
                    var name=data.toolinput[i].fields.NAME
                    var des=data.toolinput[i].fields.DESCRIPTION
                    var type=data.toolinput[i].fields.TYPE
                    var def=data.toolinput[i].fields.DEFAULT
                    var isrequired=data.toolinput[i].fields.ISREQUIRED
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
                for (var i=0;i<data.tooloutput.length;i++){
                    var name=data.tooloutput[i].fields.NAME
                    var des=data.tooloutput[i].fields.DESCRIPTION
                    var type=data.tooloutput[i].fields.TYPE

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

                return;
            }
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error",2000);


        },
    });
}


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


function updateTool() {
    var name=$('#tool_name').val();
    var type=$('#tool_type').val();
    var language=$('#tool_language').find('.span-chooice-click').html()
    var scriptCode=$('#tool_scriptCode').val();
    var des=$('#tool_des').val();
    var inputParam=INPUTPARAM;
    var outputParam=OUTPUTPARAM;
    var owner=$('#tool_owner').val()
    $.ajax({
        url:"/app_tower/workingPlatform/tool_update",
        type:"POST",
        data:{
            toolid:$('#toolid').val(),
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
                opt_commons.dialogShow("成功信息","编辑成功！",2000);
                window.location.href='/static/templates/pages/app_tower_pages/workingPlatform/toolDetail.html?toolid='+$('#toolid').val()+'&toolname='+$('#toolname').html()
                return;
            }
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error",2000);


        },
    });


}



//@ sourceURL=editTool.js