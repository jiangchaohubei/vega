/**
 * Created by PC on 2017/8/17.
 */
$(function () {
    var C1=window.location.href.split("?")[1];
    var id=C1.split("&")[0].split('=')[1];
    var name=decodeURI(C1.split("&")[1].split('=')[1]);
    $('#softwareName').html(name);
    $('#softwareId').val(id);
    $('#softwareName').prop("href", "/static/templates/pages/app_cmdb_pages/version/version.html?id="+id+"&name="+name);

    opt_commons.query_validate("#version_form");
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
                $('#VERSION_OWNER').append('<option value="'+data.projectList[i].pk+'">'+data.projectList[i].fields.NAME+'</option>')
            }

        },
        error: function(data) {
            console.log('error')
        }

    })
   
})
function on_progress(evt) {       //看这个函数之前先看upload函数。这个函数可以接收一个evt(event)对象(细节自行查询progress)，他有3个属性lengthComputable，loaded，total，第一个属性是个bool类型的，代表是否支持，第二个代表当前上传的大小，第三个为总的大小，由此便可以计算出实时上传的百分比

    if(evt.lengthComputable) {

        var loaded = parseInt(evt.loaded/evt.total*100)+"%";
        $('#pros').width(loaded);
        $('#pros').text(loaded);
        if(evt.loaded==evt.total){
            $('#ProgressModal').modal('hide');
        }
    }
}
function uploadComplete(evt) {
    /* 服务器端返回响应时候触发event事件*/

    console.log(evt.target)
    var data=JSON.parse(evt.target.responseText)
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

        opt_commons.dialogShow("成功信息","添加成功！",2000);
        $('#version_form')[0].reset();  //通过调用 DOM 中的reset方法来重置表单
        return;
    }

}
function uploadFailed(evt) {
    $('#ProgressModal').modal('hide');

    opt_commons.dialogShow("错误","error",2000);
}
function uploadCanceled(evt) {
    $('#ProgressModal').modal('hide');

    opt_commons.dialogShow("错误","canceled",2000);
}
function save_version(){
    //校验不成功
    if (!$('#version_form').valid()){
        return;
    }
    $('#ProgressModal').modal('show');
    var xhr = new XMLHttpRequest();

    var file = document.getElementById('VERSION_INPUTFILE').files[0];   //取得文件数据，而.file对象只是文件信息
    var form = new FormData();   //FormData是HTML5为实现序列化表单而提供的类，更多细节可自行查询
    form.append('file',file);
    form.append('softwareId',$('#softwareId').val());
    form.append('NAME',$('#VERSION_NAME').val());
    form.append('DESCRIPTION',$('#VERSION_DESCRIPTION').val());
    form.append('INSTALL_PATH',$('#VERSION_INSTALL_PATH').val());
    xhr.upload.addEventListener('progress',on_progress,false);
    xhr.addEventListener("load", uploadComplete, false);
    xhr.addEventListener("error", uploadFailed, false);
    xhr.addEventListener("abort", uploadCanceled, false);
    xhr.open("POST", "/app_cmdb/version/add", true);
    //xhr.setRequestHeader('X-CSRFTOKEN','{{ request.COOKIES.csrftoken }}');   //此处为Django要求，可无视，或者换成相应后台所要求的CSRF防护，不是django用户请去掉
    xhr.send(form);   //发送表单



}






//@ sourceURL=create_version.js