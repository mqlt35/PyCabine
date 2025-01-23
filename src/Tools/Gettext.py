#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")

class Gettext:
    """
    Class qui s'occupe uniquement de gérer gettext
    """
    __gettext = {}
    def InitGettext(self, domain):
        """
        Initialisation des traduction avec gettext
        """
        #Importation du module system 'gettext', et 'os'
        import gettext as __gettext
        import os as __os
        __gettext.bindtextdomain('tools', __os.getenv('WORKDIR') + '/locales')
        __gettext.textdomain('tools')
        __translation_path = __os.path.realpath(__os.getenv('WORKDIR') + '/locales')
        __t = __gettext.translation(domain, __translation_path)
        self.__gettext[domain] = __t.gettext

    def _(self, domain, message):
        """
        Encapsule la fonction de gettext.
        """
        return self.__gettext[domain](message)
    

    
def init():
    return Gettext()
