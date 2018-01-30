/**
 * Created by PC on 2018/1/30.
 */
$(function () {
    //var socket = new WebSocket('ws://' + window.location.host);
    var socket = new WebSocket('ws://106.14.157.183:8080');
    socket.onopen = function open() {
        console.log('WebSockets connection created.');
    };
    socket.onmessage = function message(event) {
        console.log(event)
        var data = JSON.parse(event.data);
        // NOTE: We escape JavaScript to prevent XSS attacks.
        var message = data['message'];
        alert(message);
    };
})






//@ sourceURL=soket.js