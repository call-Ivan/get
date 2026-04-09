import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led = 26
GPIO.setup(led, GPIO.OUT)

leds = [16, 12, 25, 17, 27, 23, 22, 24]

for led in leds:
    GPIO.setup(led, GPIO.OUT)

GPIO.output(leds, 0)

up = 5
down = 6

GPIO.setup(up, GPIO.IN)
GPIO.setup(down, GPIO.IN)

num = 0

def dec2bin(value):
    return [int(element) for element in bin(value) [2:].zfill(8)]

sleep_time = 0.2

while True:
    if GPIO.input(up):
        num += 1
        print(num, dec2bin(num))
        time.sleep(sleep_time)
    if GPIO.input(down):
        num -= 1
        print(num, dec2bin(num))
        time.sleep(sleep_time)

GPIO.output(leds, dec2bin(num))
