// Empty JS for your own code to be here
$(document).ready(function(){
alert(1);
namespace = '/test';

//Создаем сокет
var socket = io.connect('http://' + document.domain + ':' + location.port);
//Коннект
alert(socket);
    socket.on('connect', function() {
    	alert(2);
        socket.emit('my event', {data: 'I\'m connected!'});
    });
    //Лог событий
	socket.on('my response', function(msg) {
		alert(3);
		$('#log').append('<div class="alert alert-warning">Hello</div>');
	});
});
//<div class="alert alert-warning"><strong>Holy guacamole!</strong></div>