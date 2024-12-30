#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")

class Check:
    def __init__(self, api):
        #Je rend la variable _ global afin de l'utilisé 
        # partout dans la classe sans utilisé self._ (plus court)
        global _

        self.__api = api

    
    def Type(self, args : dict, throw=True):
        """
        Controle les type de la liste d'arguement:
        args = {
            'name_arg' : {
                'type' : str,
                'value': name_arg
            }
        }
        """
        import types  
        for key in args.keys():
            if args[key]['type'] == 'module':
                args[key]['type'] = types.ModuleType
            if not isinstance(args[key]['value'], args[key]['type']):
                if throw :
                    raise TypeError(
                        _("Parameter '%s' is of incorrect type: expected %s, got %s.") % 
                        (key, args[key]['type'], type(args[key]['value']))
                    )
                else:
                    return False
        return True

def init(api):
    return Check(api)
