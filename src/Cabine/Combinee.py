#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")



#Assignation du pin GPIO
GPIO_PIN_COMBINEE = 17

# Création d'une classe Combinee qui gère l'état du combinée soit il est décorché (1), soit raccroché (0)
class Combinee :
    def __init__(self):
        import RPi.GPIO as GPIO  # bibliothèque pour gérer les GPIO
        self.__GPIO = GPIO
        self.__GPIO.setmode(self.__GPIO.BCM)  # mode de numérotation des pins
        self.__GPIO.setup(GPIO_PIN_COMBINEE,self.__GPIO.IN)  # pin 17 réglée en input

        self._setStateCombi()

    # Renvoie l'état sous forme binaire
    def getStateCombi(self): 
        self._setStateCombi()
        return self.state

    def combiRaccrocher(self):
        return self.getStateCombi() == False
    
    def combiDeccrocher(self):
        return self.getStateCombi() == True
    
    # Renvoie l'état sous forme de texte.
    def getStateCombiTexte(self):
        etat_texte = ["Raccroché", "Décroché"]
        self._setStateCombi()
        return etat_texte[self.state]

    # nettoye toutes les pins.
    def clean(self):
        self.__GPIO.cleanup()

    # Fonction interne, récupère l'état du Pin Gpio.
    def _getGpioInput(self):
        import time
        time.sleep(0.01)
        return self.__GPIO.input(GPIO_PIN_COMBINEE)
    
    # Génrère un état.
    def _setStateCombi(self):
        self.state = self._getGpioInput()

def init(api):
    global _
    _ = api._
    return Combinee()