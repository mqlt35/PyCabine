#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Un bouton est branché a la pin 24, une LED est branchée
# a la pin 25.  La LED s'allume pendant que le bouton est
# enfoncé.
#
# http://electroniqueamateur.blogspot.com/2014/03/controler-les-pins-gpio-du-raspberry-pi.html


"""
J'ai apporté quelque modification afin de savoir si le téléphone est en état décrocher ou raccrocher
"""

import RPi.GPIO as GPIO  # bibliothèque pour gérer les GPIO
import time # Ajout de la bibliothèque time pour soulager le CPU

GPIO.setmode(GPIO.BCM)  # mode de numérotation des pins
GPIO.setup(17,GPIO.IN)  # pin 17 réglée en input

# Je me suis permise de mettre, les 3 instructions ci-dessous obsolètes
# afin de faire de vérifier les 2 état (raccroché et décroché) avec les instruction en bas.
def test_obsolete():
    while True:     # en boucle jusqu'à l'interruption du programme
        #GPIO.output(25,GPIO.input(24))  # allume la LED si le bouton est enfoncé
        if(GPIO.input(17)) : 
            print("décroché")
    
def newTestDecrochage():
    i=0
    etat_texte = ["Raccroché", "Décroché"]
    while True:     # en boucle jusqu'à l'interruption du programme
        #GPIO.output(25,GPIO.input(24))  # allume la LED si le bouton est enfoncé
        i = i +1    
        print("Boucle :%d , État : %s." % (i,etat_texte[GPIO.input(17)]))
        time.sleep(1)
    
newTestDecrochage()