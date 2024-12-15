#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Cabine.Locals import L

"""
Création d'une classe personalisé pour facilité le déclenchement des erreur ultérieurs.
"""

class AttributeError(AttributeError):
    def __init__(self, *args: object, name: str | None = ..., obj: object = ...) -> None:
        print("self = ", args[0])
        variable = args[0]
        
        #msg = L[""] % variable
        #print(L[__name__ + ":" + __class__.__name__ + ":VariablesNonDéfinis"])
        print(L("VariablesNonDéfinis"))
        print(L("VariablesNonDéfinisBis"))
        msg = "La variable '%s', n'a pas été définis." % variable
        if len(args) == 2 :
            msg = msg + "\n" + args[1]

        msg = msg + "\nFin du programme avec échec."

        # Fait appel au constructeur de la classe parente
        super().__init__(msg, name=name, obj=obj) 