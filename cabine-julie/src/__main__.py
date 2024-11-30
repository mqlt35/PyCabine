
# Constante afin de savoir quelle scénario lancé
SCENARIO = 2

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
            import Cabine.Scenarios.Scenario1
        case 2:
            import Cabine.Scenarios.Scenario2
        case 3:
            import Cabine.Scenarios.Scenario3

if __name__ == "__main__" :
    main()
