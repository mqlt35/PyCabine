#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")

from Cabine.Utils import Utils
import pygame
pygame.init()
from pygame import mixer 
import time

#EXTENSION_FILE_SOUND = ".wav"
EXTENSION_FILE_SOUND = ".mp3"

DEMANDE_RACCROCHER = 0
BIENVENUE = 1
WELCOME_AND_CHOICE_PUBLICATION = 2
ERROR_CHOICE_PUBLICATION = 3
ERROR_UNKNOW_CHOICE_PUBLICATION = 4
ANNONCE_ENREGISTREMENT = 5

SON = {
    DEMANDE_RACCROCHER : "demande_raccrocher_telephone",
    BIENVENUE :"son_bienvenue",
    WELCOME_AND_CHOICE_PUBLICATION: "welcome_and_choice_publication",
    ERROR_CHOICE_PUBLICATION: "error_choice_publication",
    ERROR_UNKNOW_CHOICE_PUBLICATION: "error_unknow_choice_publication",
    ANNONCE_ENREGISTREMENT: "annonce_enregistrement"
}

"""
La classe son permet de jouer différent son avec le haut parleur du combinée.
"""
class Son:

    def __init__ (self,):
        from Cabine.Factory import Factory
        self.Combi = Factory().getClass("Combinee")
        self.Touches = Factory().getClass("Touches")
        self.directorySon = Utils.getWorkDir() + "/ressources/son/"
        self.ext = EXTENSION_FILE_SOUND
        self.file = {}
        #TODO Ajouter des condition si cela fonctionne.
        mixer.init() 
        mixer.music.set_volume(0.7) 


    def loadSound(self, id) : 
        self.file[id] = self.directorySon + SON[id] + self.ext
        #TODO Ajouter des condition si cela fonctionne.
        mixer.music.load(self.file[id])

    def play(self, id) :
        self.loadSound(id)
        mixer.music.play()

    def stop(self):
        mixer.music.stop()

    def get_busy(self):
        return mixer.music.get_busy()

    def wait(self, get_key :str|None = None):
        stop = False
        #Fonction pratique pour patienter pendant l'écoute.
        #Néanmoins il est sage de pouvoir interrompre l'écoute lorsque ont appuis sur une touche définie ou
        # si çà raccroche.
        while self.get_busy():
            time.sleep(0.1)# économie du temps CPU
            if (self.Combi.getStateCombi() == False) or (get_key and get_key == self.Touches.getButtonPressed()):
                stop = True
            if (stop):
                self.stop()