/**
 * Created by PC on 2017/8/17.
 */
$(function () {

    opt_commons.query_validate("#playbook_form");
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
                $('#playbook_owner').append('<option value="'+data.projectList[i].pk+'">'+data.projectList[i].fields.NAME+'</option>')
            }

        },
        error: function(data) {
            console.log('error')
        }

    })
})
function save_playbook(){
    //校验不成功
    if (!$('#playbook_form').valid()){
        return;
    }
    var playbook_name=$('#playbook_name').val();
    var playbook_discription=$('#playbook_discription').val();
    var playbook_content=$('#playbook_content').val() ? $('#playbook_content').val():"";
    var playbook_owner=$('#playbook_owner').val();
    var playbook_dir=$('#playbook_dir').val();
    var gitlabPath=$('#playbook_gitPath').html();
    var gitProjectId=$('#playbook_gitPath').attr("gitProjectId");
    var formData = new FormData($( "#playbook_form" )[0]);
    formData.append("name",playbook_name);
    formData.append("discription",playbook_discription);
    formData.append("content",playbook_content);
    formData.append("owner",playbook_owner);
    formData.append("dir",playbook_dir);
    formData.append("gitlabPath",gitlabPath);
    formData.append("gitProjectId",gitProjectId);
    $.ajax({
        url:"/app_tower/playbook/add",
        type:"POST",
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
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
                console.log(data.resultCode)
                opt_commons.dialogShow("成功信息","添加成功！",2000);
                $('#playbook_form')[0].reset();  //通过调用 DOM 中的reset方法来重置表单
                return;
            }
        },
        error: function(data) {
                opt_commons.dialogShow("错误","error",2000);
        },
    })

}

function checkGitLabToken() {
    $.ajax({
        url:"/app_tower/playbook/gitlab_checkGitLabToken",
        type:"POST",
        data: {

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
                $('#gitlabModal').modal('show');
                return
            }
            if(data.resultCode=="0000"){
                $('#gitlabModal').modal('show');
                console.log(data)
                console.log(data.projects[0])
                $('#projectList').html("")
                $('#projectList').append("<ul>")
                $('#gitLabLogin').css("display","none");
                for(var i=0;i<data.projects.length;i++){
                    var params={}
                    params.id=data.projects[i].id
                    //params.private_token=data.private_token
                    params.path = "/"
                    $('#projectList').append("<li><a href='javascript:getCatalogue("+JSON.stringify(params)+");'>"+data.projects[i].id+"："+data.projects[i].name+"</a></li>")

                }
                $('#projectList').append("</ul>")
            }

        },
        error: function(data) {
            if(data.resultCode="0001"){
                opt_commons.dialogShow("提示信息","失败！",2000);
                console.log("error");

                return;

            }
        },
    })
}
function gitLogin() {
    var loginName=$('#playbook_gitLogin').val()
    var loginPassword=$('#playbook_gitPassword').val()
    // $('#gitlabModal').find(".modal-body").load("/app_tower/playbook/gitlab_login", {
    //     loginName:loginName,
    //     loginPassword:loginPassword,
    // });
    $.ajax({
        url:"/app_tower/playbook/gitlab_login",
        type:"POST",
        data: {
            loginName:loginName,
            loginPassword:loginPassword,
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
            console.log(data)
            console.log(data.projects[0])
            $('#gitLabLogin').css("display","none");
            $('#projectList').html("")
            $('#projectList').append("<ul>")
            for(var i=0;i<data.projects.length;i++){
                var params={}
                params.id=data.projects[i].id
                //params.private_token=data.private_token
                params.path = "/"
                $('#projectList').append("<li><a href='javascript:getCatalogue("+JSON.stringify(params)+");'>"+data.projects[i].id+"："+data.projects[i].name+"</a></li>")

            }
            $('#projectList').append("</ul>")
        },
        error: function(data) {
            if(data.resultCode="0001"){
                opt_commons.dialogShow("提示信息","失败！",2000);
                console.log("error");

                return;

            }
        },
    })
}

function getCatalogue(params) {
    console.log(11111111)
    console.log(params)
    var id=params.id;
    //var private_token=params.private_token;
    var path=params.path;

    $.ajax({
        url:"/app_tower/playbook/gitlab_getTree",
        type:"POST",
        data: {
            id:id,
            //private_token:private_token,
            path:path ? path : "",
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
            console.log(data)
            console.log(data.tree[0])
            $('#projectList').html("")
            $('#projectList').append("<ul>")
            for(var i=0;i<data.tree.length;i++){
                var param={}
                param.id=id
               // param.private_token=private_token
                if (path=='/'){
                    param.path = data.tree[i].name
                }else{
                    param.path = path+"/"+data.tree[i].name
                }
                param.i =i
                if (data.tree[i].type=="tree"){
                    $('#projectList').append("<li><a href='javascript:getCatalogue("+JSON.stringify(param)+");'>"+data.tree[i].name+"</a></li>")
                }else{
                    $('#projectList').append("<li id='projectList"+i+"' onclick='chooseFile("+JSON.stringify(param)+")'  path='"+JSON.stringify(param)+"'>"+data.tree[i].name+"</li>")
                }
            }
            $('#projectList').append("</ul>")
        },
        error: function(data) {
            if(data.resultCode="0001"){
                opt_commons.dialogShow("提示信息","失败！",2000);
                console.log("error");

                return;

            }
        },
    })

}
function chooseFile(param) {
    $('#projectList li').each(function (n,v) {
        console.log(111)
        if ( n==param.i){
            console.log(222)
            $("#projectList"+param.i).css({
                "background":"#e46262",
                "opacity":"0.7"
            })
            $(v).attr("active","true")
        }else{
            $(v).css({
                "background":"#ffffff",
                "opacity":"1"
            })
            $(v).removeAttr("active")
        }
    })


}
function beSureChooseFile() {
    var path=""
    $('#projectList li[active="true"]').each(function (n,v) {
        path=$(v).attr("path")
    })
    $('#playbook_gitPath').html(JSON.parse(path).path)
    $('#playbook_gitPath').attr("gitProjectId",JSON.parse(path).id)
}


//@ sourceURL=playbook_create.js