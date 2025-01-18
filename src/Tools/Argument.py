#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")

class Argument():
    """
    La classe "Argument" permet d'analyser la ligne de commande.

    """
    def __init__(self, api):
        import sys
        self.__api = api
        
        self.argv = sys.argv
        self.args = None
        #self.argv.pop()
        #self.args = self.parser.parse_args()

    def configure(self) : 
        _ = self.__api._
        from argparse import ArgumentParser
        self.parser = ArgumentParser(
        #self.parser = _Argument(
            prog= "cabine",
            #Voice answering machine welcoming testimonials
            description= _("description"),
            epilog= _("_epilog"),
        )
        self.sub_parser = self.parser.add_subparsers(
            dest="command",
            required=False,
            help=_("Mode d'éxécution"),
        )

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def add_args_sub_parser(self, names, **options):
      
        sub_parser = self.sub_parser.add_parser(names, help=options["help"])
        for command in options["commands"]:
            sub_parser.add_argument(*command["names"], **command["parameters"])

    def get_options(self):
        return self.args
    
    def parse_args(self):
        self.args = self.parser.parse_args()

def init(api):
    global _
    return Argument(api)