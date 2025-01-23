# options.py contient les options du programme.
from settings import SCENARIO

OPTIONS = {
    "daemon" : {
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
                    "help" : "Chemin du fichier PID (par défaut : /run/cabine/file.pid)",
                    "default" : "/run/cabine/file.pid"
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
    "service" : {
        "help"      : "Gère la mise en place du programme avec systemd.",
        "groupes" : {
            "required" : True,
            "commands" : [
                {
                    "names" : ["-i", "--install"],
                    "parameters" : {
                        "action" : "store_true",
                        "help" : f"Installe le service et l'active",
                    }
                },
                {
                    "names" : ["-u", "--uninstall"],
                    "parameters" : {
                        "action" : "store_true",
                        "help" : f"Supprime le service.",
                    }
                },
                {
                    "names" : ["-r", "--reinstall"],
                    "parameters" : {
                        "action" : "store_true",
                        "help" : f"Réinstalle le service.",
                    }
                }
            ]
        }
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