"""
Routes and views for the flask application.
"""

async_mode = None

if async_mode is None:
    try:
        import eventlet

        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey

            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

if async_mode == 'eventlet':
    import eventlet

    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey

    monkey.patch_all()

import time
from datetime import datetime
from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(2)
        count += 1
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count, 'date': str(datetime.now().time())},
                      namespace='/test')


@app.route('/')
def index():
    """Renders the home page."""
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    return render_template(
            'device.html',
            title='Home Page',
            year=datetime.now().year,
    )


@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count'], 'date': str(datetime.now().time())})


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0, 'date': str(datetime.now().time())})


if __name__ == '__main__':
    socketio.run(app,debug=True)
    #for public activity add host='0.0.0.0'
