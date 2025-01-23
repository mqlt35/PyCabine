#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Création d'une classe personalisé pour facilité le déclenchement des erreur ultérieurs.
"""

class AttributeError(AttributeError):
    def __init__(self, *args: object, name: str | None = ..., obj: object = ...) -> None:
        print("var = ", args[0])
        api = args[0]
        variable = args[1]
        msg = api._("The variable '%s', has not been defined.") % variable

        if len(args) == 3 :
            msg = msg + "\n" + args[2]

        msg = msg + api._("\nProgram ended with failure.")

        # Fait appel au constructeur de la classe parente
        
        super().__init__(msg, name=name, obj=obj) 