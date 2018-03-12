function feedback(){
    var topic=$("#topic").val();
    var content=$("#content").val();
    if(topic&&content){
             $.ajax({
                url: "/feedback/saveFeedBack",
                type: "POST",
                data: {
                    TOPIC: topic,
                    CONTENT: content,
                },
                dataType: "json",
                success: function (data) {
                    if (data.resultCode=="0087"){
                        alert(data.resultDesc);
                        top.location.href ='/login'
                    }
                    if (data.resultDesc == "Success") {
                        opt_commons.dialogShow("成功信息", "您反馈的宝贵意见我们会尽快改正", 2000);
                        $("#topic").val("");
                        $("#content").val("");
                        return;
                    }
                },
                 error: function(data) {
                     opt_commons.dialogShow("错误", "服务器错误！", 1000);
                 },
            });
    }else{
        opt_commons.dialogShow("提示信息", "请输入您的主题和您宝贵的意见！", 2000);
    }



}


// 到  出所有的反馈意见
function exportFeedback(){
       $.ajax({
                url: "/feedback/export/allFeedback",
                type: "POST",
                dataType: "json",
                success: function (data) {
                    if (data.resultCode=="0087"){
                        alert(data.resultDesc);
                        top.location.href ='/login'
                    }
                    if (data.resultDesc == "Success") {
                        opt_commons.dialogShow("成功信息", "导出成功!", 2000);
                        downloadExcel(data.filepath);
                        return;
                    }
                },
           error: function(data) {
               opt_commons.dialogShow("错误", "服务器错误！", 1000);
           },
            });
}


function downloadExcel(filepath){
        window.open("/feedback/export/allFeedback/download?filepath="+filepath);
}