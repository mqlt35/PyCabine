#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Cabine.Factory import Factory
from time import sleep

from enum import Enum
class State(Enum):
    RACCROCHER=1
    DECROCHER=2
    CHOICE_PUBLICATION_OK=3

#Condition afin de savoir quel touches du clavier matriciel sont accepter.
CHOICE_PUBLICATION_ACCEPTED = [1, 2]

class Scenario1() :
    # Attribut de classe pour stocker l'unique instance
    _instance = None

    def __new__(self, *args, **kwargs):
        # Vérifie si une instance existe déjà
        # merci Chat GPT
        if not self._instance:
            self._instance = super(Scenario1, self).__new__(self, *args, **kwargs)
            pass
        return self._instance
    
    def __init__(self):
         # A initialiser qu'une seule fois.
         if not hasattr(self, "_initialized"):
            self._initialized = True
            self.Son = Factory().getClass("Son")
            self.Combi = Factory().getClass("Combinee")
            self.Touches = Factory().getClass("Touches")
            self.Enregistrement = Factory().getClass("Enregistrement")
            self.choice_publication = None
            self.state = State.RACCROCHER


    def exec(self):
        if self.state == State.RACCROCHER :
            #Condition si le téléphone n'est pas décrocher, alors j'envoie l'annonce d'acceuil
            if not self.attenteDecrochage() :
                #raise Exception("Erreur inconnue : Je n'ai pas reçue l'état du téléphone\nIl est censé renvoyé toujours True")
                return False
        elif self.state == State.DECROCHER :
            self.Touches.load()
            # Le téléphone est décrocher.

            #Envoie de l'annonce de bienvenue
            # Dans ce scénarion j'envoie un son de bienvenue 
            # avec la demande pour choisir le type de publication
            # TODO : J'ai mis une pause, a terme modifier la bande son
            sleep(2)
            self.sendWelcomeAnnounceAndChoicePublication()
        elif self.state == State.CHOICE_PUBLICATION_OK:
            self.Enregistrement.setFile(self.choice_publication)
            self.Son.play(self.Son.ANNONCE_ENREGISTREMENT)
            self.Son.wait()
            self.Touches.unload()
            self.Enregistrement.saveVocalMsg()

            # Le choix de publication à été fait, on peut poursuivre.
            if self.choice_publication == 1 :
                print("La publication sur internet est choisie")
            elif self.choice_publication == 2 :
                print("Mode secret activé.")


            # A des fin de test.
            # laisse à laps de temps pour raccrocher.
            print("Pause maximal 5 seconde, cela devrais laisser le temps de raccrocher.")
            secondes = 0
            while secondes <= 5:
                sleep(1)
                secondes +=1
                if self.Combi.combiRaccrocher():
                    break
            self.state = State.RACCROCHER
            
        if self.state == State.RACCROCHER :
            # Fin du scénario
            #Déchargement des touches du clavier
            self.Touches.unload()
            self.state = State.RACCROCHER
            self.choice_publication = None
        
    def getVocalMessage(self):
        pass
    def sendWelcomeAnnounceAndChoicePublication(self):
            # Lancement du message de bienvenue.
            # TODO : J'envoie l'annonce de bienvenue.
            self.Son.play(self.Son.WELCOME_AND_CHOICE_PUBLICATION)

            while not self.choice_publication:
                sleep(0.1)

                #Si 1 ou 2 à été appuyer alor
                # s'assurer que le son est arrêté
                # puis définir le choix de publication
                # traiter les erreurs si mauvaise touche appuyer, puis recommencer.
                touche = self.Touches.getButtonPressed()
                if self.Combi.combiRaccrocher():
                    # Cas 1 : Le téléphone est raccrocher.
                    self.Son.stop()
                    self.state = State.RACCROCHER #On reprend à 0
                    print("Choix publication : Téléphone raccrocher.")
                    break
                elif not self.Son.get_busy():
                    # Le son est finis alors je lance à nouveau la demande pour faire un choix
                    print("Choix publication : Le délai est dépassé.")
                    self.Son.play(self.Son.ERROR_UNKNOW_CHOICE_PUBLICATION)
                elif touche in CHOICE_PUBLICATION_ACCEPTED :
                    self.choice_publication = self.Enregistrement.ChoicePublication(touche)
                    self.Son.stop()
                    self.state = State.CHOICE_PUBLICATION_OK
                    print("Choix publication : un choix à été fait.")
                elif touche != None and not touche in CHOICE_PUBLICATION_ACCEPTED :
                    # Mauvais choix, je lance à nouveau la demande.
                    print("Choix publication : Mauvais Choix.")
                    self.Son.play(self.Son.ERROR_CHOICE_PUBLICATION)
        # Fin de méthode : sendWelcomeAnnounceAndChoicePublication

    # TODO Si le téléphone est décrocher le programme boucle jusqu'à ce qu'il sois raccrocher
    def attenteDecrochage(self, _sleep : int|None= None):
        if (self.Combi.combiDeccrocher()) : 
            print("Le téléphone est déjà décrocher, en attente pour qu'il soit raccrocher.")
            # Une pause demander avant de relancer l'annonce
            #  (uniquement dans le cas où la fonction est rappeler dans la condition.)
            if _sleep :
                sleep(_sleep)
            # Lance une annonce vocale (téléphone décrocher)
            self.Son.play(self.Son.DEMANDE_RACCROCHER)
            #On attend la fin de la lectue ou que la personne raccroche.
            self.Son.wait()

            #Le téléphone est toujours décrocher, on retourne dans la même fonction avec une pause de 2 secondes
            self.attenteDecrochage(2)
        
        print("En service, le programme attend qu'une personne décroche.")
        # Boucle while jusq'à ce que le combinée soit décrocher
        while True: #Point de départ du programme en temps normal.
            sleep(0.1)# économie du temps CPU
            combinee_decrocher = self.Combi.getStateCombi()
            if combinee_decrocher == True :
                print("Téléphone décrocher : Retour au scénario.")
                self.state = State.DECROCHER
                return combinee_decrocher


def lancement(module):
    scenar = module.Scenario1()
    scenar.exec()
