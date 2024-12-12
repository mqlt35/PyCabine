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

SON = {
    DEMANDE_RACCROCHER : "demande_raccrocher_telephone"
}

"""
La classe son permet de jouer différent son avec le haut parleur du combinée.
"""
class Son:

    def __init__ (self,):
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
