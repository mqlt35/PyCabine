#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Constante afin de savoir quelle scénario lancé
from Tools import utils
from Cabine import C_ as _
SCENARIO = 1
Debug = True
Path = "s"
#utils = None
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

def createArgument():
    factory = utils.getFactory()
    list_args = {
        "deamon" : {
            "choices": ["start", "stop", "status", "reload"],
            "help" : _("Message d'aide")
        }
    }

    args = "deamon"
    kwargs = {
        "choices": ["start", "stop", "status", "reload"],
        "help" : _("Message d'aide")
        
    }
    factory('Argument', 'add_argument', args, **kwargs)
    factory('Argument', 'parse_args')
    print(factory('Argument', 'get_args'))
    pass
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

def main2():
    factory = utils.getFactory()
    createArgument()
    
    test_args=['arg1', 'arg2']
    #print(factory("Argument", method='get_args', args=test_args))
    factory("Argument", "args")
    #print(_Utils(cls='Argument',method='get_args'))
    pass
if __name__ == "__main__" :
    main2()
    utils.Clean()
    exit()
    #TODO Test de la classe Langue, le but est de renvoyer un texte
    try:
        main()
    except KeyboardInterrupt:
        print("Fin du programme")
        Utils.Clean()
