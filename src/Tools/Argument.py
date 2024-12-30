#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")

class Argument():
    """
    La classe "Argument" permet d'analyser la ligne de commande.

    """
    def __init__(self):
        import sys
        from argparse import ArgumentParser
        from Tools import _
        
        self.argv = sys.argv
        self.args = None
        #self.argv.pop()
        self.parser = ArgumentParser(
        #self.parser = _Argument(
            prog= "cabine",
            #Voice answering machine welcoming testimonials
            description= _("description"),
            epilog= _("_epilog")
        )
        #self.args = self.parser.parse_args()

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def get_args(self):
        return self.args
    
    def parse_args(self):
        self.args = self.parser.parse_args()

def init(api):
    global _
    _ = api._
    return Argument()