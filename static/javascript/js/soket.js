/**
 * Created by PC on 2018/1/30.
 */
$(function () {
    $.ajax({
        url:"/app_tower/message/select",
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
                $('#messageNum').html(data.messageNum)
                for (var i=0;i<data.messageList.length;i++){
                    $('#messagelist').prepend(
                        '<li>'+
                        '<div class="text-center link-block">'+
                        '<a href="#">'+
                        '<i class="glyphicon glyphicon-envelope"></i>'+
                        '<span style="word-wrap:break-word;word-break:break-all; ">'+data.messageList[i].fields.CONTENT+'</span>'+
                        '</a>'+
                        '</div>'+
                        '</li>'
                    )
                }

                return;
            }

            socket_connet();
        },

        error:function(data){
            opt_commons.dialogShow("错误信息","error",2000);


        },
    });


})

function socket_connet() {
    var socket = new WebSocket('ws://' + window.location.host);
    socket.onopen = function open() {
        console.log('WebSockets connection created.');
    };
    socket.onmessage = function message(event) {
        console.log(event)
        var data = JSON.parse(event.data);
        // NOTE: We escape JavaScript to prevent XSS attacks.
        var message = data['message'];
        var type=data['type']

        var messageNum=parseInt($('#messageNum').html())+1
        $('#messageNum').html(messageNum)
        $('#messagelist').prepend(
            '<li>'+
            '<div class="text-center link-block">'+
            '<a href="#">'+
            '<i class="glyphicon glyphicon-envelope"></i>'+
            '<span style="word-wrap:break-word;word-break:break-all; ">'+message+'</span>'+
            '</a>'+
            '</div>'+
            '</li>'
        )
        console.log(message)
    };
    socket.onerror = function(e) {
        console.log(e);
    };
    socket.onclose = function(e) {
        console.log("connection closed");
    };
    if (socket.readyState == WebSocket.OPEN) {
        socket.onopen();
    }
}





//@ sourceURL=soket.js