#!/usr/bin/env python3
#-- coding: utf-8 --
import platform
import time

# GPIO and cross-platform development
if platform.system()=='Linux': # raspberry
 	from RPi import GPIO
else: # macos or stg else...
    import dummy_gpio_sim.dummygpiosim as GPIO

# TODO : check https://www.framboise314.fr/scratch-raspberry-pi-composants/gpio/
BUTTON_PIN = 21

def init_gpio():
    GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board)

    GPIO.setwarnings(False) #On désactive les messages d'alerte

    # ref doc
    # https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/

    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, bouncetime=1000)  

def main_run():
    init_gpio()

    try:
        while True:

            if GPIO.input(BUTTON_PIN):
                print('Input was HIGH')
            else:
                print('Input was LOW')
            
            time.sleep(1)  # wait 1s to give CPU chance to do other things

            # if GPIO.event_detected(BUTTON_PIN):
            #     print('START (Physical button pressed)')

    except KeyboardInterrupt:
        pass
        GPIO.cleanup()

if __name__ == '__main__':
    print("#### BEGIN")
    main_run()
    print("#### END")