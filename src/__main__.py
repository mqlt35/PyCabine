#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Constante afin de savoir quelle scénario lancé
from Cabine.Utils import Utils
from Cabine.Locals import L

SCENARIO = 1
Debug = True
Path = "s"
"""
Ce fichier ne s'occupe que de lancer le scénario sur lequel je travail.

Scénario 1 - témoignage simple
Scénario 2 - témoignage avec possibilité de réécoute et de modification
Scénario 3 - témoignage avec choix thématiques
"""

def erreur():
    print("Une erreur c'est produite pendant l'initialisation de l'un des 3 scénaris")

def quiterProgramme() :
    while True :
        value = input("\n(q to quit or enter to continue) > ")
        if value == "q":
            print("Bye")
            return True
        elif value == "":
            print("\n")
            return False

    
def main():
    #Switch qui décide quelle scénario lancé.
    match SCENARIO:
        case 1:
            from Cabine.Scenarios import Scenario1 as Scenario
        case 2:
            from Cabine.Scenarios import Scenario2 as Scenario
        case 3:
            from Cabine.Scenarios import Scenario3 as Scenario
    
    while True :
        Scenario.lancement(Scenario)

        # A commenter lorsque le programme sera lancer en arrière plan
        #FIXME: Trouver un moyen de quiter le programme proprement à la fin de service
        # NOTE: Une solution en ajoutant un bouton, celui-ci arrêtra le programme, puis le raspberry?
        #if(quiterProgramme()):
        #    break

if __name__ == "__main__" :
    Utils.init()
    #print(Utils.baseName.__doc__)
    #print(L("HelloWorld"))
    #exit()
    #TODO Test de la classe Langue, le but est de renvoyer un texte
    try:
        main()
    except KeyboardInterrupt:
        print("Fin du programme")
        Utils.Clean()
