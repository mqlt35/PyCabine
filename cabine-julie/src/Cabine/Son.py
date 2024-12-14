#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Cabine.Utils import Utils
import pygame
pygame.init()
from pygame import mixer 
import time

#EXTENSION_FILE_SOUND = ".wav"
EXTENSION_FILE_SOUND = ".mp3"

DEMANDE_RACCROCHER = 0
BIENVENUE = 1

SON = {
    DEMANDE_RACCROCHER : "demande_raccrocher_telephone",
    BIENVENUE :"son_bienvenue"
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

    def wait(self, get_key :str|None = None):
        stop = False
        #Fonction pratique pour patienter pendant l'écoute.
        #Néanmoins il est sage de pouvoir interrompre l'écoute lorsque ont appuis sur une touche définie ou
        # si çà raccroche.
        while mixer.music.get_busy():
            time.sleep(0.1)# économie du temps CPU
            if (self.Combi.getStateCombi() == False) or (get_key and get_key == self.Touches.getButtonPressed()):
                stop = True
            if (stop):
                self.stop()