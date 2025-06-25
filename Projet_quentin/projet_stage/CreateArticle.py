import requests
from requests.auth import HTTPBasicAuth
import ssl
import os
from datetime import datetime
import importlib
import subprocess
import sys

site_url = "https://mqlt.fr"
api_url = f"{site_url}/wp-json/wp/v2/posts"
categories_url = f"{site_url}/wp-json/wp/v2/categories"
tags_url = f"{site_url}/wp-json/wp/v2/tags"
media_url = f"{site_url}/wp-json/wp/v2/media"
username = "cabine"
app_password = "M1pS LsLQ dn2N O9s6 ALw7 lU5M"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE 

session = requests.Session()
session.verify = False 

headers = {
    'User-Agent': 'Python WordPress Client',
    'Accept': 'application/json',
}

def formater_date(chaine):
    """Formate le nom de fichier en une date lisible"""
    if chaine.endswith('.mp3'):
        chaine = chaine[:-4]
    
    parties = chaine.split('_')
    if len(parties) >= 3 and parties[0].isdigit():
        chaine = '_'.join(parties[1:])
        parties = chaine.split('_')
    
    if len(parties) < 2:
        return chaine
    
    date_part = parties[0]
    heure_part = parties[1]
    
    try:
        date_obj = datetime.strptime(date_part, '%d-%m-%Y')
        heure_obj = datetime.strptime(heure_part, '%H-%M-%S')
        
        mois_fr = [
            'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
            'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'
        ]
        
        jour = date_obj.day
        mois = mois_fr[date_obj.month - 1]
        annee = date_obj.year
        
        heure = heure_obj.hour
        minute = heure_obj.minute
        
        return f"{jour} {mois} {annee} à {heure}h{minute:02d}"
    except ValueError:
        return chaine

def upload_media_to_wordpress(file_path, media_type='image'):
    """Upload un fichier (image ou audio) vers WordPress"""
    try:
        if not os.path.exists(file_path):
            print(f"Fichier {media_type} introuvable: {file_path}")
            return None
            
        with open(file_path, 'rb') as file:
            response = session.post(
                media_url,
                auth=HTTPBasicAuth(username, app_password),
                files={'file': (os.path.basename(file_path), file)},
                headers={
                    'Content-Disposition': f'attachment; filename={os.path.basename(file_path)}',
                    'Content-Type': f'audio/mpeg' if media_type == 'audio' else 'image/jpeg'
                }
            )
        
        if response.status_code == 201:
            if media_type == 'audio':
                return response.json().get('source_url')
            return response.json().get('id')
        else:
            print(f"Erreur lors de l'upload {media_type}: {response.text}")
            return None
    except Exception as e:
        print(f"Erreur lors de l'upload {media_type}: {str(e)}")
        return None

def get_or_create_category(category_name):
    params = {'search': category_name}
    response = session.get(categories_url, 
                         auth=HTTPBasicAuth(username, app_password),
                         headers=headers,
                         params=params)
    
    if response.status_code == 200:
        categories = response.json()
        for category in categories:
            if category['name'].lower() == category_name.lower():
                return category['id']
            
    data = {'name': category_name}
    response = session.post(categories_url,
                          auth=HTTPBasicAuth(username, app_password),
                          headers=headers,
                          json=data)
    
    if response.status_code == 201:
        return response.json().get('id')
    else:
        print(f"Erreur lors de la création de la catégorie: {response.text}")
        return None

def get_or_create_tag(tag_name):
    params = {'search': tag_name}
    response = session.get(tags_url, 
                         auth=HTTPBasicAuth(username, app_password),
                         headers=headers,
                         params=params)
    
    if response.status_code == 200:
        tags = response.json()
        for tag in tags:
            if tag['name'].lower() == tag_name.lower():
                return tag['id']
            
    data = {'name': tag_name}
    response = session.post(tags_url,
                          auth=HTTPBasicAuth(username, app_password),
                          headers=headers,
                          json=data)
    
    if response.status_code == 201:
        return response.json().get('id')
    else:
        print(f"Erreur lors de la création de l'étiquette: {response.text}")
        return None

def create_post(audio_filename, image_filename=None, categorie=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_path = os.path.join(script_dir, "audio", audio_filename)
    
    # Upload de l'audio
    audio_url = upload_media_to_wordpress(audio_path, 'audio')
    if not audio_url:
        print("Échec de l'upload de l'audio")
        return False

    # Formatage du titre et de la date
    formatted_date = formater_date(audio_filename)
    
    # Upload de l'image si elle existe
    featured_media = None
    if image_filename:
        image_path = os.path.join(script_dir, "image", image_filename)
        if os.path.exists(image_path):
            featured_media = upload_media_to_wordpress(image_path)

    excerpt = f"Témoignage enregistré le {formatted_date}"
    
    content = f"""
    <div class="testimonial-container">
        <div class="testimonial-header">
            <a href="{site_url}/?p=%post_id%" class="testimonial-title-link">
                <h1>{formatted_date}</h1>
            </a>
        </div>
        
        <span class="listen-text">Ecouter le témoignage</span>
        
        <div class="audio-player-container">
            <div class="audio-player">
                [audio src="{audio_url}"]
            </div>
        </div>
        
        <div class="divider"></div>
    </div>
    """
    
    post_data = {
        "title": f"Témoignage du {formatted_date}",
        "content": content,
        "excerpt": excerpt,
        "status": "publish",
        "comment_status": "open"
    }
    
    if featured_media:
        post_data["featured_media"] = featured_media
    
    if categorie:
        category_id = get_or_create_category(categorie)
        if category_id:
            post_data['categories'] = [category_id]
    

    try:
        response = session.post(api_url,
                            auth=HTTPBasicAuth(username, app_password),
                            json=post_data,
                            headers=headers,
                            timeout=30)
        
        if response.status_code == 201:
            post_id = response.json().get('id')
            post_link = response.json().get('link')
            
            # Mettre à jour le contenu avec le bon lien
            updated_content = content.replace('%post_id%', str(post_id))
            update_data = {
                'content': updated_content
            }
            update_response = session.post(f"{api_url}/{post_id}",
                                        auth=HTTPBasicAuth(username, app_password),
                                        json=update_data,
                                        headers=headers)
            
            print(f"Article créé avec succès")
            print("Lien :", post_link)
            print("ID :", post_id)
            return True
        else:
            print(f"Erreur HTTP {response.status_code}")
            print("Réponse serveur :", response.text)
            return False

    except requests.exceptions.SSLError as e:
        print(f"Erreur SSL:", str(e))
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion:", str(e))
        return False

    except Exception as e:
        print(f"Erreur inattendue:", type(e).__name__, "-", str(e))
        return False

def process_files():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_dir = os.path.join(script_dir, "audio")
    image_dir = os.path.join(script_dir, "image")

    if not os.path.exists(audio_dir):
        print(f"Le dossier audio n'existe pas: {audio_dir}")
        return
    
    if not os.path.exists(image_dir):
        print(f"Le dossier image n'existe pas: {image_dir}")
        return
    
    # Filtrer les fichiers audio pour exclure ceux commençant par "2"
    audio_files = [f for f in os.listdir(audio_dir) 
                  if f.lower().endswith('.mp3') and not f.startswith('2')]
    
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    image_dict = {os.path.splitext(f)[0]: f for f in image_files}
    
    for audio_file in audio_files:
        audio_base = os.path.splitext(audio_file)[0]
        image_file = image_dict.get(audio_base)
        
        success = create_post(audio_file, image_file, categorie="Cabine de témoignages")
        
        if success:
            print(f"Article créé pour {audio_file}")
    
    # Exécution de UploadFichier.py après le traitement des fichiers
    run_upload_script()

def run_upload_script():
    """Exécute UploadFichier.py dans un processus séparé"""
    try:
        print("\nDémarrage de l'exécution de UploadFichier.py...")
        
        # Chemin absolu vers le script
        script_path = os.path.join(os.path.dirname(__file__), "UploadFichier.py")
        
        # Exécution avec capture de la sortie
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Affichage des résultats
        print("Sortie de UploadFichier.py:")
        print(result.stdout)
        if result.stderr:
            print("Erreurs:", result.stderr)
            
        print("UploadFichier.py exécuté avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erreur d'exécution (code {e.returncode}):")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"Erreur inattendue: {str(e)}")
        return False

if __name__ == "__main__":
    process_files()