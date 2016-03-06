"""
Routes and views for the flask application.
"""

async_mode = None



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
import RPi.GPIO as GPIO
from datetime import datetime
from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

pin = 18
led_pin = 23
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.IN)
GPIO.setup(led_pin,GPIO.OUT)
led_state = False
count = 0
def eventgpio(pin):
    global count, led_state, led_pin
    if (led_state):
        GPIO.output(led_pin,led_state)
        led_state = not led_state
    else:
        GPIO.output(led_pin,led_state)
        led_state = not led_state
    
    count += 1
    socketio.emit('my response',
                      {'data': 'Falling', 'count': count, 'date': str(led_state)},
                      namespace='/test')
    
GPIO.add_event_detect(pin,GPIO.FALLING,callback = eventgpio,bouncetime = 100)

@app.route('/')
def index():
    """Renders the home page."""
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
    socketio.run(app, host = '0.0.0.0')
