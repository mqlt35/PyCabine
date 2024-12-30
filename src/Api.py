#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")

"""
Ce fichier agit comme un chef d’orchestre pour coordonner les modules principaux (À savoir Tools et Cabine) tout en évitant les 
importations cycliques et en centralisant les interactions inter-modules. L'objectif est de maintenir une 
structure claire, modulaire et facile à maintenir.
"""

from Tools import Gettext
from settings import MODULES, EXCEPTIONS # Import de configuration externe

class Api:
    """
    Classe de gestion principale reliant les outils (Tools) et les modules du projet principal (Cabine).
    
    Responsabilités :
        - Centraliser les interactions entre les modules.
        - Gérer les initialisations et la configuration.
        - Agir comme interface pour les appels extérieurs (API).
    """

    #Gestion des domaines pour gettext
    __list_allowed_modules_for_gettext = {}

    def __init__(self):
        """
        Initialisation de tous les modules utilisés dans le projet.
        """
        # Initialisation de gettext
        self.__gettext = Gettext.init()
        for domain in ['cabine', 'tools', 'error']:
            self.__gettext.InitGettext(domain)

        # Autoriser les classes d'exception à utiliser gettext
        self.__allow_exceptions_use_gettext()
        
        # Charger les modules principaux et leurs éléments
        self.__tools = self.__import_all_modules(MODULES["tools"])
        self.__mods_projects = self.__import_all_modules(MODULES["projects"])
        self.__scenarios = list(self.__import_all_modules(MODULES["scenarios"]).values())

        # Regrouper toutes les classes initialisées
        self.__list_cls_initialized = [
            self.__gettext, *self.__tools.values(),
            *self.__mods_projects.values(),
            *self.__scenarios,
        ]

    def __import_dynamic(self, module_name):
        """
        Importe dynamiquement un module à partir de son nom sous forme de chaîne.
        
        Args:
            module_name (str): Nom complet du module (e.g., 'Cabine.Scenarios.Scenario1').
        
        Returns:
            Module: Une référence au module importé.
        """
        try:
            components = module_name.split('.')
            domain = components[0].lower()
            module = __import__('.'.join(components[:-1]), fromlist=[components[-1]])
            self.__allow_use_gettext(domain, module_name)
            return getattr(module, components[-1])
        except (ImportError, AttributeError) as e:
            raise ImportError(self.__("Error importing module %s : %s") % (module_name, e))
    
    def __import_all_modules(self, module_names):
        """
        Importe plusieurs modules donnés par une liste de noms et configure leurs autorisations pour gettext.
        
        Args:
            module_names (list[str]): Liste des noms complets des modules à importer.
        
        Returns:
            dict[str, Module]: Dictionnaire associant les noms courts des modules à leurs objets importés.
        """
        modules = {}
        for module_name in module_names:
            _, name = module_name.rsplit('.', 1)
            module = self.__import_dynamic(module_name)
            modules[name] = module.init(self) if hasattr(module, 'init') else module
        return modules

    def __allow_exceptions_use_gettext(self):
        """
        Ajoute une autorisation pour chaque classe d'exception présent dans le tableau 'EXCEPTIONS'
        du fichier 'setting.py'
        """
        domain = 'error'
        for name_cls_exception in EXCEPTIONS :
            name = 'Exceptions.' + name_cls_exception
            self.__allow_use_gettext(domain, name)

    def __allow_use_gettext(self, domain_gettext, *names_caller_modules):
        """
        Ajoute un ou plusieurs modules à la liste des modules autorisés pour un domaine gettext donné.
        
        Args:
            domain_gettext (str): Le domaine de gettext (e.g., 'cabine', 'tools').
            names_caller_modules (str): Un ou plusieurs noms de modules autorisés.
        """
        if domain_gettext not in self.__list_allowed_modules_for_gettext:
            self.__list_allowed_modules_for_gettext[domain_gettext] = []
        
        self.__list_allowed_modules_for_gettext[domain_gettext].extend(names_caller_modules)

    def _(self, message):
        """
        Encapsule la méthode '_' de la classe Gettext pour les traductions.
        
        Args:
            message (str): Texte à traduire.
        
        Returns:
            str: Texte traduit si le module appelant est autorisé, sinon le texte original.
        """
        __name_caller_module = self.getTools_Utils().GetCallingModule()
        for domain, list_names_modules in self.__list_allowed_modules_for_gettext.items():
            if __name_caller_module in list_names_modules : 
                return self.__gettext._(domain,message)
        return message
    
    def __(self, message):
        """
        Tips : méthode interne pour forcer l'utilisation de gettext exclusivement dans ce module.
        Encapsule la méthode '_' de la classe Gettext pour les traductions.
        
        Args:
            message (str): Texte à traduire.
        
        Returns:
            str: Texte traduit.
        """
        return self.__gettext._('tools', message)
    def configure(self):
        for _cls in self.__list_cls_initialized :
            if hasattr(_cls, 'configure'):
                configure = getattr(_cls, 'configure')
                if callable(configure):
                    configure()
    
    # Accesseurs pour les modules principaux  
    def GetCls_Combiner(self):
        return self.__mods_projects['Combinee']
    
    def GetCls_Son(self):
        return self.__mods_projects['Son']
    
    def GetCls_Touches(self):
        return self.__mods_projects['Touches']
    
    def GetCls_Enregistrement(self):
        return self.__mods_projects['Enregistrement']
    
    # Accesseurs pour les outils  
    def getTools_Utils(self):
        return self.__tools['Utils']
    
    def getTools_Check(self):
        return self.__tools['Check']
    
    def getTools_Argument(self):
        return self.__tools['Argument']
    
    def getTools_Mixer(self):
        return self.__tools['Mixer']
        
    
    def RunScenario(self,__id_scenario):
        """
        Exécute un scénario sélectionné par son ID.
        
        Args:
            __id_scenario (int): ID du scénario (à partir de 1).
        """
        while True:
            """ 
            TODO:
            //    A terme ce programme et donc se scénario pourra être arrêté par les cas suivant: 
            //    - manuellement avec 'systemctl stop cabine'
            //    - Avec le gestionnaire cachée : Appuie sur la touche # -> 1 (arrêt programme puis système)
            //    - Lorsque l'on fait la combinaison 'Ctrl+C', met fin au programme.
            """

            try:
                self.__scenarios[__id_scenario - 1].exec()
            except KeyboardInterrupt:
                # A commenter lorsque le programme sera lancer en arrière plan
                #FIXME: Trouver un moyen de quiter le programme proprement à la fin de service
                # NOTE: Une solution en ajoutant un bouton, celui-ci arrêtra le programme, puis le raspberry?
                #if(quiterProgramme()):
                print("Ctrl+C à été déclancher pour mettre un terme au programme.")
                break


# Factory pour l'initialisation du projet
def initialiser_projet():
    """
    Initialise et configure l'API du projet.

    Returns:
        Api: Instance configurée de la classe Api.
    """
    api = Api()
    api.configure()
    return api