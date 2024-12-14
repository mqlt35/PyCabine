#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Cabine import Combinee as Combi
from Cabine.Factory import Factory
import time

class Scenario1 :
    def __init__(self):
        self.Son = Factory().getClass("Son")
        self.Combi = Factory().getClass("Combinee")
        self.Touches = Factory().getClass("Touches")

        #Condition si le téléphone n'est pas décrocher, alors j'envoie l'annonce d'acceuil
        #Chargement des touches du clavier
        self.Touches.load()
        if not self.attenteDecrochage() :
            #raise Exception("Erreur inconnue : Je n'ai pas reçue l'état du téléphone\nIl est censé renvoyé toujours True")
            return False
        
        # Le téléphone est décrocher.

        #Envoie de l'annonce de bienvenue
        self.sendWelcomeAnnounce()

        while True:
            time.sleep(0.5)
            button = self.Touches.getButtonPressed()
            if button : 
                print(button)
            if (button == self.Touches.NAME_KEYPAD["#"]):
                break


        # Fin du scénario
        #Déchargement des touches du clavier
        self.Touches.unload()
        etatCombi = self.Combi.getStateCombi()
        print("L'état du combiné est à %d." % etatCombi)
        

    def sendWelcomeAnnounce(self):
            # Lancement du message de bienvenue.
            # TODO : J'envoie l'annonce de bienvenue.
            self.Son.play(self.Son.BIENVENUE)
            # Attendre que le son se termine (ou que le téléphone sois raccrocher).
            # ou encore que la touche '*' soit enclencher.
            self.Son.wait(self.Touches.NAME_KEYPAD['*'])

    # TODO Si le téléphone est décrocher le programme boucle jusqu'à ce qu'il sois raccrocher
    def attenteDecrochage(self, _sleep : int|None= None):
        if (self.Combi.getStateCombi() == True) : 
            print("Le téléphone est déjà décrocher, en attente pour qu'il soit raccrocher.")
            # Une pause demander avant de relancer l'annonce
            #  (uniquement dans le cas où la fonction est rappeler dans la condition.)
            if _sleep :
                from time import sleep
                sleep(_sleep)
            # Lance une annonce vocale (téléphone décrocher)
            self.Son.play(self.Son.DEMANDE_RACCROCHER)
            #On attend la fin de la lectue ou que la personne raccroche.
            self.Son.wait()

            #Le téléphone est toujours décrocher, on retourne dans la même fonction avec une pause de 2 secondes
            self.attenteDecrochage(2)
        
        print("En service, le programme attend qu'une personne décroche.")
        # Boucle while jusq'à ce que le combinée soit décrocher
        while True:
            time.sleep(0.1)# économie du temps CPU
            combinee_decrocher = self.Combi.getStateCombi()
            if combinee_decrocher == True :
                print("Téléphone décrocher : Retour au scénario.")
                return combinee_decrocher


def lancement(module):
    return module.Scenario1()
