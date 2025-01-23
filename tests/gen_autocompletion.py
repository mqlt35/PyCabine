import sys
import shutil
import subprocess
import re
import os

def get_program_path(program):
    """
    Retourne le chemin absolu d'un programme s'il existe dans le PATH.
    """
    return shutil.which(program)


def run_help_command(program, extra_args=None):
    """
    Essaie différentes commandes pour obtenir l'aide d'un programme.
    """
    commands = [["--help"], ["-h"], ["help"]]
    if extra_args:
        commands = [extra_args + cmd for cmd in commands]

    for cmd in commands:
        try:
            result = subprocess.run(
                [program] + cmd, capture_output=True, text=True
            )
            if result.returncode == 0:  # Succès
                return result.stdout
        except Exception:
            continue
    return None


def parse_help_output(output):
    """
    Analyse la sortie du programme pour identifier les options, sous-commandes et arguments.
    """
    # Nouvelle regex pour capturer à la fois les options et les sous-commandes
    #options = re.findall(r'(--\w+|-{1,2}\w+)', output)
    options = re.findall(r'(w+|-{2}\w+)\s*?', output)
    #subcommands = re.findall(r'(?<=\s)(daemon|service|load)(?=\s)', output)
    commands = re.findall(r"^\s+([\w]+)\s{2}", output, re.MULTILINE)
    
    return sorted(set(options)), sorted(set(commands))

def generate_bash_completion(program, structure):
    """
    Génère un script de complétion Bash basé sur la structure du programme.
    """
    structure = {
        'options': ['--help', '-h' ], 
        'commands':  ['daemon', 'load', 'service'], 
        'sub_commands': {
            'daemon': {
                'options': ['--help', '--pidfile', '--scenario', '-h', '-p', '-s'], 
                'commands': ['ninja'], 
                'sub_commands': {}
            }, 
            'load': {
                'options': ['--help', '--scenario', '-h', '-s'], 
                'commands': ['biloute'], 
                'sub_commands': {}
            }, 'service': {
                'options': ['--help', '--install', '--reinstall', '--uninstall', '-h', '-i', '-r', '-u'], 
                'commands': [], 'sub_commands': {}
            }
        }
    }

    def recurse_commands(name, level, struct):
        script = ""

        if "options" in struct:
            opts = " ".join(struct["options"])
            script += f"{'  ' * level}opts_{name}=\"{opts}\"\n"


        if "sub_commands" in struct:
            subs = " ".join(struct["commands"])
            script += f"{'  ' * level}subs_{name}=\"{subs}\"\n"
            for sub, substruct in struct["sub_commands"].items():
                script += recurse_commands(f"{name}_{sub}", level + 1, substruct)
        return script

    script = f"""#!/bin/bash
    _{program}_completion() {{
        local cur prev
        COMPREPLY=()
        cur="${{COMP_WORDS[COMP_CWORD]}}"
        prev="${{COMP_WORDS[COMP_CWORD-1]}}"
        opts=""
        pos=""

"""
    # Génération récursive du contenu
    script += recurse_commands(program, 1, structure)

    # Ajout des règles de complétion
    script += f"""
    case "$cur" in
        /*|./*|../*|~/*) # Si l'utilisateur tape un chemin
            COMPREPLY=( $(compgen -f -- "$cur") )
            return 0
            ;;
    esac
    
    case "$prev" in
"""
    for sub, substruct in structure.get("sub_commands", {}).items():
        script += f"        {sub}) opts=\"$opts_{program}_{sub} $subs_{program}_{sub}\" ;;\n"
        print(substruct)

    script += f"        *) opts=\"$opts_{program} $subs_{program}\" ;;\n"
    script += """    esac

    COMPREPLY=( $(compgen -W "$opts" -- $cur) )
    return 0
}
"""
    script += f"complete -F _{program}_completion {program}\n"

    return script

def explore_program_structure(program, args=None, depth=0, max_depth=3):
    """
    Explore récursivement la structure des commandes et sous-commandes.
    """
    if depth > max_depth:  # Limite de profondeur atteinte
        return {}

    output = run_help_command(program, args)
    if not output:
        return {}
   # Analyser les options et les sous-commandes
    options, commands = parse_help_output(output)

    structure = {"options": options, "commands": commands, "sub_commands" : {}}


    # Explorer récursivement chaque sous-commande
    for sub in commands:
        structure["sub_commands"][sub] = explore_program_structure(
            program, args=(args or []) + [sub], depth=depth + 1, max_depth=max_depth
        )
    return structure

if __name__ == '__main__' :
    if len(sys.argv) != 2:
        print("Utilisation : python gen_autocompletion.py <nom_programme> .")
        sys.exit(1)

    nom_programme = sys.argv[1]

    # Obtenir le chemin absolu du programme
    program_path = get_program_path(nom_programme)

    if not program_path:
        print(f"Erreur : Le programme '{nom_programme}' n'est pas disponible sur le système.")
        sys.exit(1)

    print(f"Programme trouvé : {program_path}")
    # Explorer la structure
    #structure = explore_program_structure(program_path)
    #print(structure)

    structure = True
    if structure:
        bash_script = generate_bash_completion(os.path.basename(program_path), structure)
        script_name = f"{nom_programme}_completion.sh"
        with open(script_name, "w") as file:
             file.write(bash_script)
        print(f"Script de complétion Bash généré : {script_name}")
    else:
        print("Aucune structure détectée.")