$(document).ready(function () {
    namespace = '/test'; // change to an empty string to use the global namespace
    //alert(1);
    var count = 0;
    // the socket.io documentation recommends sending an explicit package upon connection
    // this is specially important when using the global namespace
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    socket.on('my response', function (msg) {
        //alert(2);
            //$('#log').fadeIn('slow', function(){
                //$(this).append('<div class="alert alert-info" id=' + count + '>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data + '-' + msg.date).html());
            //});
            var eventText = $('<div class="alert alert-info" id=' + count
                                + '>' + 'Received #' + msg.count + ': ' + msg.data
                                + '-' + msg.date + '<div/><div/>').hide();
            $('#log').append(eventText);
            eventText.fadeIn('slow');

            count++;

            if ( count >= 6) {
                //alert(55);
                var elem = document.getElementById(count - 6);
                //$(elem).fadeOut(800,function(){
                    //$(this).remove();
                //});

                //$(elem).slideUp('slow',function(){
                    //$(this).remove();
                //});

                $(elem).fadeTo("slow", 0.00, function(){
                    $(this).slideUp('slow',function(){
                        $(this).remove();
                    });
                });
            }
    });

    // event handler for new connections
    socket.on('connect', function () {
        //alert(3);
        socket.emit('my event', { data: 'I\'m connected!' });
    });

    // handlers for the different forms in the page
    // these send data to the server in a variety of ways
});