# options.py contient les options du programme.
from settings import SCENARIO

OPTIONS = {
    "deamon" : {
        "help"       :   "Gère le programme comme un daemon.",
        "commands" : [
            {
                "names" : ["action"],
                "parameters" : {
                    "choices" : ["start", "stop", "restart", "status"],
                    "type" : str,
                    "help" : "Action sur le démon"
                    },
            },
            {
                "names" : ["-p", "--pidfile"],
                "parameters" : {
                    "type" : str,
                    "help" : "Chemin du fichier PID (par défaut : /var/run/cabine/file.pid)",
                    "default" : "/var/run/cabine/file.pid"
                }
            },
            {
                "names" : ["--statusfile"],
                "parameters" : {
                    "type" : str,
                    "help" : "Chemin du fichier de statut (par défaut : /var/run/cabine/file.status)",
                    "default" : "/var/run/cabine/file.status"
                }
            },
            {
                "names" : ["-s", "--scenario"],
                "parameters" : {
                    "default" : SCENARIO,
                    "type" : int,
                    "help" : f"Exécute le scénario sélectionné. (par défaut : {SCENARIO})",
                    "choices" : [1, 2, 3]
                }
            }
        ],
        
    },
    "load" : {
        "help"       :   "Démarre le programme.",
        "commands" : [
            {
                "names" : ["-s", "--scenario"],
                "parameters" : {
                    "default" : SCENARIO,
                    "type" : int,
                    "help" : f"Exécute le scénario sélectionné. (par défaut : {SCENARIO})",
                    "choices" : [1, 2, 3]
                }
            }
        ]
    }
}