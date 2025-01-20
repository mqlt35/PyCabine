#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")


class GPIO:
    def __init__(self, api):
        import RPi.GPIO as GPIO  # bibliothèque pour gérer les GPIO
        # Associer la fonction de gestion des touches au clavie
        self.__api = api
        self.__GPIO = GPIO

    def pre_run(self):
        self.__GPIO.setmode(self.__GPIO.BCM)

    def setup(self, pin, mode, **args):
        self.__GPIO.setup(pin, mode, **args)

    def input(self, pin):
        return self.__GPIO.input(pin)
    
    def add_event_detect(self, *args, **kwargs):
        self.__GPIO.add_event_detect(*args, **kwargs)

    def cleanup(self):
        self.__GPIO.cleanup()

    def __getattr__(self, name):
        # Ignorer les attributs non solicités
        if name in ("configure", "post_configure"):  # Ajouter les attributs non solicités
            return super().__getattr__(name)
        elif name in self.__GPIO.__dict__:
           # print(name)
            return getattr(self.__GPIO, name)
        else:
            raise AttributeError(f"GPIO object has no attribute {name}")
    
def init(api):
    return GPIO(api)