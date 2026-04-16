import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# leds = 26

# GPIO.setup(leds, GPIO.OUT)

leds = [16, 12, 25, 17, 27, 23, 22, 24]

for led in leds:
    GPIO.setup(leds, GPIO.OUT)

GPIO.output(leds,0)

up = 19
down = 26

GPIO.setup(up, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(down, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

num = 0

def dec2bin(value):
    return [int(element) for element in bin(value) [2:].zfill(8)]

sleep_time = 0.2

try:
    while True:
        # проверяем одновременного нажатия кнопок
        if GPIO.input(up) and GPIO.input(down):
            num = 255
            print(num, dec2bin(num))
            time.sleep(sleep_time)
        else:
            if GPIO.input(up):
                num+=1
                if num > 255:
                    num = 0
                print(num,dec2bin(num))
                time.sleep(sleep_time)
            
            if GPIO.input(down):
                num-=1
                if num < 0:
                    num = 255
                print(num,dec2bin(num))
                time.sleep(sleep_time)
        GPIO.output(leds,dec2bin(num))

except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nThat's all")