#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Constante afin de savoir quelle scénario lancé
SCENARIO = 1
Debug = True

"""
Ce fichier ne s'occupe que de lancer le scénario sur lequel je travail.

Scénario 1 - témoignage simple
Scénario 2 - témoignage avec possibilité de réécoute et de modification
Scénario 3 - témoignage avec choix thématiques
"""

def erreur():
    print("Une erreur c'est produite pendant l'initialisation de l'un des 3 scénaris")

def main():
    #Switch qui décide quelle scénario lancé.
    match SCENARIO:
        case 1:
            from Cabine.Scenarios import Scenario1
        case 2:
            from Cabine.Scenarios import Scenario2
        case 3:
            from Cabine.Scenarios import Scenario3

if __name__ == "__main__" :
    main()
