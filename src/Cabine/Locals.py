#!/usr/bin/env python
# -*- coding: utf-8 -*-

#TODO ce fichier peut être importer dans plusieur scripte, je crain des imports Ciruclaire
#@see https://docs.kanaries.net/fr/topics/Python/python-circular-import


"""
Fichier contenant tous les messages afficher à l'écran, étant donnée mes problèmes d'ortographe
cela facilitera la maintenance et corriger les erreurs de texte.

ATTENTION, ne pas modifier les clef, justes les valeurs du dictionnnaire.
"""

"""
L = {
    # src/Cabine/

    # src/Exceptions/AttributeError.py
    "Exceptions.AttributeError:AttributeError:dd" : "La variable '%s', n'a pas été définis."
}
"""


from typing import Any

def L(key):
    if not hasattr(Langue, "initialiser") : 
        Langue.initialiser = Langue()

    return Langue.initialiser.getItem(key)

class Langue :
    def __init__ (self) :
        pass


    def getItem(self, name: str) -> Any:
        import sys
        from Tools.Utils import Utils
        caller = {
            "class" : sys._getframe(2).f_code.co_qualname,
            "file" : Utils.baseName(sys._getframe(2).f_code.co_filename)
        }
        print(caller)
        print(name)
        return "bidule"