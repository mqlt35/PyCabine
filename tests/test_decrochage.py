#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Un bouton est branché a la pin 24, une LED est branchée
# a la pin 25.  La LED s'allume pendant que le bouton est
# enfoncé.
#
# http://electroniqueamateur.blogspot.com/2014/03/controler-les-pins-gpio-du-raspberry-pi.html

import RPi.GPIO as GPIO  # bibliothèque pour gérer les GPIO

GPIO.setmode(GPIO.BCM)  # mode de numérotation des pins
GPIO.setup(17,GPIO.IN)  # pin 17 réglée en input

while True:     # en boucle jusqu'à l'interruption du programme
    #GPIO.output(25,GPIO.input(24))  # allume la LED si le bouton est enfoncé
    if(GPIO.input(17)) : 
        print("décroché")
    