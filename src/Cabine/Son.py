#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")

"""
La classe son permet de jouer différent son avec le haut parleur du combinée.
"""
class Son:
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
    def __init__ (self, api):
        self.__api = api
        self.ext = self.EXTENSION_FILE_SOUND
        self.file = {}
        #TODO Ajouter des condition si cela fonctionne.

    def configure(self):
        self.directorySon = self.__api.getTools_Utils().getWorkDir() + "/ressources/son/"
        self.__mixer = self.__api.getTools_Mixer()
        self.__combi = self.__api.GetCls_Combiner()
        self.__touches = self.__api.GetCls_Touches()

    def loadSound(self, id) : 
        self.file[id] = self.directorySon + self.SON[id] + self.ext
        self.__mixer.load_music(self.file[id])

    def play(self, id) :
        self.loadSound(id)
        self.__mixer.play_music()

    def stop(self):
        self.__mixer.stop_music()

    def get_busy(self):
        return self.__mixer.get_busy_music()

    def wait(self, get_key :str|None = None):
        stop = False
        #Fonction pratique pour patienter pendant l'écoute.
        #Néanmoins il est sage de pouvoir interrompre l'écoute lorsque ont appuis sur une touche définie ou
        # si çà raccroche.
        from time import sleep
        while self.get_busy():
            sleep(0.1)# économie du temps CPU
            if (self.__combi.getStateCombi() == False) or (get_key and get_key == self.__touches.getButtonPressed()):
                stop = True
            if (stop):
                self.stop()

def init(api):
    global _
    _ = api._
    return Son(api)