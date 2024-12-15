#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")

# J'ai juste besoin du module PATH
from os import path
from Cabine.Exceptions.AttributeError import AttributeError

#TODO ce fichier peut être importer dans plusieur scripte, je crain des imports Ciruclaire
#@see https://docs.kanaries.net/fr/topics/Python/python-circular-import

class Utils:
    """
    La classe 'Utils' est une classe utilitaire qui soulage le codeur sur la répétion.

    La classe est dites static, il n'y a pas lieu de l'initialiser, 

    ---------------------------- Liste Méthodes Static gérent les nom de chemins -----------------------
    -->  getWorkDir() : Renvoie le répertoire de travail du projet, déclenche une Exception de type 'AttributeError'
                        si initWorkdir n'a pas été appelé.
    """
    def Clean():
        from Cabine.Factory import Factory
        touches = Factory().getClass("Touches")
        combi = Factory().getClass("Combinee")
        touches.clean()
        combi.clean()

    """
    =====================================================================================================================
    ====                                                                                                             ====
    ====                   Définition de Méthode  utilitaire pour la gestion des noms de chemins.                    ====
    ====                                                                                                             ====
    =====================================================================================================================
    """


    def getWorkDir() -> str:
        """
            Récupère le répertoire de travail du projet
        Raises:
            AttributeError: initWorkdir n'a pas été appelé, un déclenchement d'erreur s'impose pour éviter des bug ultérieur

        Returns:
            str: Renvoie Utils.WorkDir définis dans la méthode statiqued initWorkdir()
        """
        if not hasattr(Utils, "WorkDir") :
            raise AttributeError("Utils.WorkDi", "Avez-vous fait appel à la méthode static 'Utils.setWorkDir() ?")            
        return Utils.WorkDir
    
    def baseName(file: str, without_ext: bool | None = ...) -> str:
        basename = path.basename(file)

        if without_ext == True:
            basename = basename.split('.')[0]
            print(basename)
            print(without_ext)
        return basename
    

    """
    =====================================================================================================================
    ====                                                                                                             ====
    ====                           Fonction D'initialisation du projet                                               ====
    ====                  Elle sont appellé une seule fois dans le programme (@see __main__.py)                      ====
    ====                                                                                                             ====
    =====================================================================================================================
    """
    def initWorkDir():
        """
            Méthode statique afin de définire le répertoire principale de travail du Projet PyCabine.
            Pour cela cette méthode doit être lancée au scripte principal et évité tout problème
        """
        Utils.WorkDir = path.realpath(path.dirname(__file__) + "/../..")

    def init():
        """
            Méthode d'initialisation, permet d'initialiser le projet si il y a lieu (@see src/__main__.py)        
        """
        Utils.initWorkDir()
        from Cabine.Factory import Factory
        factory = Factory()
        factory.getClass("Touches")
        factory.getClass("Combinee")
        # TODO: ajouter des instruction ci-dessous servant à initialiser le projet.

"""
=====================================================================================================================
====                                                                                                             ====
====                                  Fin de la classe 'Utils'                                                   ====
====                                                                                                             ====
=====================================================================================================================
"""

