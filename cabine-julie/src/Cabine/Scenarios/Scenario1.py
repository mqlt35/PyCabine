#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Cabine import Combinee as Combi
from Cabine.Factory import Factory

class Scenario1 :
    def __init__(self):
        self.Classes = {
            "Son" : {
                    "Module" : Factory.getModule("Son"),
                    "Classe" : Factory.getClass("Son")
            }
        }
        combi = Combi.Combinee()
        self.attenteDecrochage(combi) 
        #TODO  Est-ce utile de faire une condition???

        # TODO : J'envoie l'annonce de bienvenue.
        etatCombi = combi.getStateCombi()

        print("L'état du combiné est à %d." % etatCombi)
        combi.cleanup()

    # TODO Si le téléphone est décrocher le programme boucle jusqu'à ce qu'il sois raccrocher
    def attenteDecrochage(self, combi):
        # Je boucle tant que le combiné est racroché
        if (combi.getStateCombi() == True) : 
            print("Veuillez d'abord raccrocher le téléphone")
            # Lancer une annonce vocale (téléphone décrocher)
            Son = self.Classes["Son"]
            """ModuleSon = Factory.getModule("Son")
            ClasseSon = Factory.getClass("Son")
            ClasseSon.play(ModuleSon.DEMANDE_RACCROCHER)"""
            Son["Classe"].play(Son["Module"].DEMANDE_RACCROCHER)

            #Son.Son(Son.DEMANDE_RACCROCHER)
            return False
        
        print("En attente d'un témoignage. Status téléphone Raccorcher")
        # Boucle while jusq'à ce que le combinée
        while (combi.getStateCombi() == False):
            pass
        print("Le combiné est décroché.")
        etatCombi = combi.getStateCombi()
        return etatCombi


def lancement(module):
    module.Scenario1()
