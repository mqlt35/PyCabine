#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")

import importlib

class Factory(object) :
    # Attribut de classe pour stocker l'unique instance
    _instance = None

    # Liste des classes chargées 
    # une seule fois
    listClasses = {}
    def __new__(cls, *args, **kwargs):
        # Vérifie si une instance existe déjà
        if not cls._instance:
            cls._instance = super(Factory, cls).__new__(cls, *args, **kwargs)
           # print("Nouvelle instance de Factory créée.")
        else:
            #print("Instance existante de Factory utilisée.")
            pass
        return cls._instance
    
    def __init__(self):
        # Init ne s'exécute qu'une seule fois si nécessaire
        if not hasattr(self, "_initialized"):
            self._initialized = True
            #print("Factory initialisée")

    @staticmethod
    def loadClasse(module, name_classe) : 
        # Charge la classe depuis un module
        return getattr(module, name_classe)

    @staticmethod
    def getModule(name_module) :
        # Charge dynamiquement un module
        name_module = "Cabine." + name_module
        return importlib.import_module(name_module)
    
    def getClass(self, name_classe) : 
        # Récupère le module et la classe
        module = self.getModule(name_classe)
        classe = self.loadClasse(module, name_classe)

        # Attacher toutes les constantes au niveau de la classe
        for attr in dir(module):
            if attr.isupper():  # Filtres les constantes (majuscules)
                setattr(classe, attr, getattr(module, attr))

        # Si la classe n'est pas chargé, alors, je la charge ici.
        if name_classe not in self.listClasses:
            #print(f"Chargement de la classe {name_classe}")
            self.listClasses[name_classe] = classe()


        return self.listClasses[name_classe]
    

    """
            def __getattr__(self, name):
        # Intercepte les attributs inexistants
        print(f"__getattr__ appelé pour : {name}")
       
        return None

    def __getattribute__(self, name):
        # Intercepte tous les accès aux attributs
        print(f"__getattribute__ appelé pour : {name}")
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        # Intercepte toutes les modifications d'attribut
        print(f"__setattr__ appelé pour : {name} = {value}")
        super().__setattr__(name, value)

    def __call__(self, *args, **kwargs):
        # Rend l'objet appelable comme une fonction
        print(f"Factory appelée avec arguments : {args} et {kwargs}")
    """