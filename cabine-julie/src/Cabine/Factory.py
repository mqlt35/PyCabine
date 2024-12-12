#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")

import importlib

listClasses = {
    "Son" : None
}


class Factory :
    
    def __init__() :
        # Initialisation des Classe à chager qu'une seule fois
        pass

    def loadClasse(module, name_classe) : 
        return getattr(module, name_classe)

    def getClass(name_classe) : 
        # Récupère le module et la classe
        module = Factory.getModule(name_classe)
        classe = Factory.loadClasse(module, name_classe)
        
        # Si la classe n'est pas chargé, alors, je la charge ici.
        if (isinstance(listClasses[name_classe], classe) == False) :
            print("Classe non définie")
            loader = classe()
            listClasses[name_classe] = loader


        return listClasses[name_classe]
    
    def getModule(name_module) :
        name_module = "Cabine." + name_module
        return importlib.import_module(name_module)