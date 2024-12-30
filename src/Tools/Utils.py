#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")

#from Tools import _
from Exceptions.AttributeError import AttributeError

#TODO ce fichier peut être importer dans plusieur scripte, je crain des imports Ciruclaire
#@see https://docs.kanaries.net/fr/topics/Python/python-circular-import

class Utils:
    """
    La classe 'Utils' est une classe utilitaire qui soulage le codeur sur la répétion.

    --> __new__() création de l'instance
    --> __init__() Initialisation de l'instance
    --> clean() Nettoie les objets des classes crée : Voir la méthode "clean" de chaque classes.

        ---------------------------- Liste Méthodes Static gérent les nom de chemins -----------------------
        
    -->  getWorkDir() : Renvoie le répertoire de travail du projet, déclenche une Exception de type 'AttributeError'
                        si initWorkdir n'a pas été appelé.
    """
    # Attribut de classe pour stocker l'unique instance
    _instance = None


    """
    =====================================================================================================================
    ====                                                                                                             ====
    ====                           Fonction D'initialisation du projet                                               ====
    ====              Elle sont appellé une seule fois dans le programme (@see src/Tools/__init__.py)                ====
    ====                                                                                                             ====
    =====================================================================================================================
    """


    """
    Méthode qui permet de crée l'instance, cette instance sera unique.
    """
    def __new__(cls, _, *args, **kwargs):
        # Vérifie si une instance existe déjà
        if not cls._instance:
            cls._instance = super(Utils, cls).__new__(cls, *args, **kwargs)
           # print("Nouvelle instance de Factory créée.")
        else:
            #print("Instance existante de Factory utilisée.")
            pass
        return cls._instance

    """
    Méthode pour initialiser l'instance, celle-ci sera unique.
    La classe est appelé et initialisé depuis "src/Tools/__init__.py"
    """
    def __init__(self, api, *args, **kwargs):
        # Init ne s'exécute qu'une seule fois si nécessaire
        if not hasattr(self, "_initialized"):
            self._initialized = True
            super().__init__(*args, **kwargs)
            # J'ai juste besoin du module PATH
            from os import path as _path
            self._path = _path
            self.__api = api
            self.WorkDir = self._initWorkDir()
            """
            from Tools.Factory import Factory
            self.factory = Factory()
            self._cls_touches = self.factory.getClassCabine("Touches")
            self._cls_combinee = self.factory.getClassCabine("Combinee")
            self._cls_argument = self.factory.getTool("Argument")

            self._list_cls_to_clean = ['_cls_touches', '_cls_combinee']
            """
            
            # TODO: ajouter des instruction ci-dessous servant à initialiser le projet.
            print("Utils à été initialisé.")
    def configure(self):
        global _
        _ = self.__api._

    def _initWorkDir(self):
        """
            Méthode privée afin de définire le répertoire principale de travail du Projet PyCabine.
            Pour cela cette méthode doit être lancée au scripte principal et évité tout problème
        """
        return self._path.realpath(self._path.dirname(__file__) + "/../..")

    """
    =====================================================================================================================
    ====                                                                                                             ====
    ====                                        Fonction public (Api)                                                ====
    ====                                                                                                             ====
    =====================================================================================================================
    """

    @staticmethod
    def GetCallingModule(throw : bool = False):
        """
        GetCallingModule Méthode statique
        Renvoie le nom du module précédent qui à appelé cette méthode à travers un autre module

        Exemple : La méthode 'lancement' du module 'Cabine.Scenarios.Scenario1',
            appelle la méthode '_' du module 'Api', qui appelle à son tour,
            la méthode d'ici (GetCallingModule)
        """
        import inspect
        #récupération de la frame actuel
        frame = inspect.currentframe()
        #Je récupère la frame appellante qui à appellée cette méthode depuis une méthode précédente.
        caller_frame = frame.f_back.f_back
        #Je récupère le module appelant
        caller_module = inspect.getmodule(caller_frame)
        #puis je renvoie son nom
        return caller_module.__name__ if caller_module else None

    @staticmethod
    def GetFirstNameModule(name_module: None | str):
        if not name_module : return None
        list_names_modules = name_module.split('.')
        return list_names_modules[0]

    def getFactory(self):
        if hasattr(self,'factory'):
            return self.factory
        
        raise Exception(_("The Factory class was not properly initialized"))

    """
    Cette méthode permet de nettoyer les classes, valeur.
    lèbère les ressources
    """
    def Clean(self) -> None :
        #boucle la liste des classes qui doit être nettoyé.
        for _cls in self._list_cls_to_clean :
            #Récupération de l'objet qui à été initialisé plus haut
            _o_cls = getattr(self, _cls)
            # Je m'assure que la méthode "clean" existe dans la liste des classes à nettoyé.
            if hasattr(_o_cls, "clean") :
                #Je récupère la méthode clean, puis je l'appelle.
                getattr(_o_cls, "clean")()

    """
    =====================================================================================================================
    ====                                                                                                             ====
    ====                   Définition de Méthode  utilitaire pour la gestion des noms de chemins.                    ====
    ====                                                                                                             ====
    =====================================================================================================================
    """

    def getWorkDir(self) -> str:
        """
            Récupère le répertoire de travail du projet
        Raises:
            AttributeError: initWorkdir n'a pas été appelé, un déclenchement d'erreur s'impose pour éviter des bug ultérieur

        Returns:
            str: Renvoie Utils.WorkDir définis dans la méthode statiqued initWorkdir()
        """
        if not hasattr(self, "WorkDir") :
            raise AttributeError(self.__api, "Utils.WorkDir", _("Did you call the static 'Utils.setWorkDir()' method?")) 
        return self.WorkDir
    
    
    def baseName(self, file: str, without_ext: bool | None = ...) -> str:
        basename = self.path.basename(file)

        if without_ext == True:
            basename = basename.split('.')[0]
            print(basename)
            print(without_ext)
        return basename

"""
=====================================================================================================================
====                                                                                                             ====
====                                  Fin de la classe 'Utils'                                                   ====
====                                                                                                             ====
=====================================================================================================================
"""


def init(api):
    return Utils(api)
