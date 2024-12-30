#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("This script is not executable.")

class Mixer :
    def __init__(self, api):
        self.__api = api
        import pygame as _pygame
        self.__pygame = _pygame
        self.__mixer = _pygame.mixer
        self.__music = _pygame.mixer.music

        
        self.__mixer.init(frequency=44100, size=-16, channels=1)
    
    def configure(self):
        global _
        _ = self.__api._

    def load_music(self, filename, namehint = ""):
        self.__music.load(filename, namehint)

    def play_music(self, loops=0,start=0.0, fade_ms=0):
        self.__music.play(loops,start, fade_ms)

    def get_busy_music(self):
        return self.__music.get_busy()
    
    def get_busy_mixer(self):
        return self.__mixer.get_busy()
    
    def stop_music(self):
        return self.__music.stop()
    
    def make_sound(self, wave):
        return self.__pygame.sndarray.make_sound(wave)

def init(api):
    return Mixer(api)