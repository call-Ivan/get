import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led = 26
GPIO.setup(led, GPIO.OUT)

phototrans = 6
GPIO.setup(phototrans, GPIO.IN)

state = 0
# period = 1.0

while True:
    sensor_value = GPIO.input(phototrans)
    state = not sensor_value
    GPIO.output(led,state)
    time.sleep(0.2)
