$(document).ready(function () {
    namespace = '/test'; // change to an empty string to use the global namespace
    var count = 0;
    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    socket.on('my response', function (msg) {
            var eventText = $('<div class="alert alert-info" id=' + count
                                + '>' + 'Received #' + msg.count + ': ' + msg.data
                                + '-' + msg.date + '<div/><div/>').hide();
            $('#log').append(eventText);
            eventText.fadeIn('slow');
            count++;
            if ( count >= 6) {
                var elem = document.getElementById(count - 6);
                $(elem).fadeTo("slow", 0.00, function(){
                    $(this).slideUp('slow',function(){
                        $(this).remove();
                    });
                });
            }
    });
    // event handler for new connections
    socket.on('connect', function () {
        socket.emit('my event', { data: 'I\'m connected!' });
    });
});