#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")

class Scenario3() :
    # Attribut de classe pour stocker l'unique instance
    _instance = None

    def __new__(self, _, *args, **kwargs):
        # Vérifie si une instance existe déjà
        # merci Chat GPT
        if not self._instance:
            self._instance = super(Scenario3, self).__new__(self, *args, **kwargs)
            pass
        return self._instance
    
    def __init__(self, api):
         # A initialiser qu'une seule fois.
         if not hasattr(self, "_initialized"):
            self._initialized = True

    def exec(self):
        print("Scenario3 : Lancement scénario 3.")

def init(api):
    global _
    _ = api._
    return Scenario3(api)