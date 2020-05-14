import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

print("Started")

PUL_pin = 16
DIR_pin = 18

# setup pins for output
GPIO.setup(PUL_pin, GPIO.OUT)
GPIO.setup(DIR_pin, GPIO.OUT)

# set both pins to high
GPIO.output(PUL_pin, GPIO.HIGH)
GPIO.output(DIR_pin, GPIO.HIGH)

# loop a bunch of times
for i in range(0, 20571):
    GPIO.output(PUL_pin, GPIO.LOW)
    time.sleep(0.001)
    GPIO.output(PUL_pin, GPIO.HIGH)
    time.sleep(0.001)
    print("loop", i)

# exit
GPIO.cleanup()