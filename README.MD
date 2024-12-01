
Voir
 [Programmation d'une cabine téléphonique anglaise - cabine de témoignages](https://www.wiki-rennes.fr/Programmation_d%27une_cabine_t%C3%A9l%C3%A9phonique_anglaise_-_cabine_de_t%C3%A9moignages)

Scénario : [Scénarios de fonctionnement de la cabine](https://docs.google.com/document/d/18E6q68mggDVUanxJHCBvNwsLgTKLPwkZbg_32MTsQv0/edit?usp=sharing)

Charte : [Charte Cabine Téléphonique de Témoignage](https://docs.google.com/document/d/1E6yp78fg-NJzNdO4ea2fbqAL292Jvwdpw8ky-wRRURM/edit?usp=sharing)


---

## Environnement de développement

Afin d'éviter de polluer le dépôt git, j'utilise environnement de virtuelle de python

```BASH
python -m venv $HOME/venv
```

Pour lancer l'environnement virtuelle de python faire :

```BASH
source $HOME/venv/bin/activate
```

Pour quiter l'environnement virtuelle faire :

```BASH
deactivate
```
## Exigences

### Modules python

Pour installer les modules, lancer la commande `python -r requirements.txt` en particulier dans l'environnement virtuelle

#### Attention

Le module `sounddevice` nécessite l'installation du paquet `libportaudio2`
