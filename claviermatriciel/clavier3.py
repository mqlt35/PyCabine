# import required libraries
import RPi.GPIO as GPIO
import time

# these GPIO pins are connected to the keypad
# change these according to your connections!
L1 = 5
L2 = 6
L3 = 13
L4 = 19

C1 = 16
C2 = 20
C3 = 21


def init():
    # Initialize the GPIO pins

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(L1, GPIO.OUT)
    GPIO.setup(L2, GPIO.OUT)
    GPIO.setup(L3, GPIO.OUT)
    GPIO.setup(L4, GPIO.OUT)

    # Make sure to configure the input pins to use the internal pull-down resistors

    # GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(C1, GPIO.BOTH, callback=CChanged, bouncetime=200)
    GPIO.add_event_detect(C2, GPIO.BOTH, callback=CChanged, bouncetime=200)
    GPIO.add_event_detect(C3, GPIO.BOTH, callback=CChanged, bouncetime=200)


def CChanged(channel):
    print("up or down for ", channel)


init()

while True:
  value = input("(q to quit) > ")
  if value == "q":
    break

print("Bye")
GPIO.cleanup()  