import RPi.GPIO as GPIO

pin = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(pin,GPIO.IN)

def evhandle(pin):
    print "Falling!"

GPIO.add_event_detect(pin,GPIO.FALLING,callback = evhandle,bouncetime = 100)

while True:
    pass
