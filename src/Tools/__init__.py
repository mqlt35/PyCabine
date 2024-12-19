"""
Tools : Ensemble d'outils pour facilité le codage ultérieur.


- Le module Factory, présente une classe qui facilite l'appel des classe qui doit être chargé une seule fois
- Le module Argument
"""


from Tools.Factory import Factory
from Tools.Utils import Utils
#from Tools.Argument import Argument


#__all__ (mot clé important)
# permet de charger les classe directement dans ce fichier init sans passer par les modules.
#__all__ = [Factory, Utils, Argument]
__all__ = [Factory, Utils]