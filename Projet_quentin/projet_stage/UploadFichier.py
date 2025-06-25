import os
import sys
import shutil
from datetime import datetime
import smbc

# Configuration des chemins ABSOLUS
if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuration
CONFIG = {
    'NAS': {
        'IP': "",
        'SHARE': "",
        'USERNAME': "",
        'PASSWORD': "",
        'REMOTE_PATH': "audio_sauvegarde"
    },
    'PATHS': {
        'AUDIO': os.path.join(SCRIPT_DIR, "audio"),
        'BACKUP': os.path.join(SCRIPT_DIR, "backup"),
        'PRIVE': os.path.join(SCRIPT_DIR, "privé")
    }
}

def init_dirs():
    """Crée les répertoires nécessaires"""
    for dir_key in ['AUDIO', 'BACKUP', 'PRIVE']:
        os.makedirs(CONFIG['PATHS'][dir_key], exist_ok=True)

def log(message):
    """Journalisation des opérations"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def upload_to_nas(file_path):
    """Transfert vers le NAS via SMB (python3-smbc)"""
    try:
        # Configuration du contexte SMB
        ctx = smbc.Context()
        ctx.optionNoAutoAnonymousLogin = True
        ctx.optionUseKerberos = False

        # Authentification
        auth_data = f"{CONFIG['NAS']['USERNAME']}:{CONFIG['NAS']['PASSWORD']}@{CONFIG['NAS']['IP']}"
        remote_dir = f"smb://{auth_data}/{CONFIG['NAS']['SHARE']}/{CONFIG['NAS']['REMOTE_PATH']}/"
        remote_path = f"{remote_dir}{os.path.basename(file_path)}"

        # Tentative de création du dossier
        try:
            ctx.mkdir(remote_dir)
        except:
            pass

        # Transfert du fichier
        with open(file_path, 'rb') as local_file:
            fd = ctx.open(remote_path, os.O_WRONLY | os.O_CREAT)
            fd.write(local_file.read())
            fd.close()

        log(f"NAS: Transfert réussi - {os.path.basename(file_path)}")
        return True

    except Exception as e:
        log(f"ERREUR NAS: {str(e)}")
        return False

def transfer_file(file_path):
    """Gère la copie de sauvegarde et le transfert NAS"""
    filename = os.path.basename(file_path)
    
    try:
        # 1. Copie vers backup
        backup_path = os.path.join(CONFIG['PATHS']['BACKUP'], filename)
        shutil.copy2(file_path, backup_path)
        log(f"Backup réussi: {filename}")
        
        # 2. Transfert NAS
        if upload_to_nas(file_path):
            os.remove(file_path)
            log(f"Suppression réussie: {filename}")
            return True
        return False
        
    except Exception as e:
        log(f"ERREUR traitement {filename}: {str(e)}")
        return False

if __name__ == "__main__":
    init_dirs()
    log("Démarrage du script")
    
    audio_dir = CONFIG['PATHS']['AUDIO']
    if not os.path.exists(audio_dir):
        log(f"ERREUR: Dossier audio introuvable {audio_dir}")
        sys.exit(1)
    
    for filename in os.listdir(audio_dir):
        file_path = os.path.join(audio_dir, filename)
        
        if not os.path.isfile(file_path):
            continue
            
        if filename.lower().endswith('.wav'):
            try:
                os.remove(file_path)
                log(f"Fichier .wav supprimé: {filename}")
            except Exception as e:
                log(f"ERREUR suppression .wav: {filename} - {str(e)}")
            continue
            
        transfer_file(file_path)
    
    log("Script terminé")