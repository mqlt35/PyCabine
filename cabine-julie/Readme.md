# Projet Cabine Téléphonqiue

## Étape du projet

- [ ] Initialisation du projet
  - [ ] Gestion des erreurs
  - [ ] Création de la classe utilitaire "Utils.py"
  - [ ] Gestion des Locales (Langue) "Locals.py"- il n'y a pas lieu de traduction, mais éventuellement de correction de fautes
  - [ ] Gestion de l'état du Combinée (raccroché, décrocher) "Combinee.py"
  - [ ] Gestion du son
  - [ ] Gestion du clavier matricielle
  - [ ] Gestion de l'enregistrement
  - [ ] Mise en place de test GPIO
- [ ] Programmation des scénarios
  - [ ] Scénario 1 (témoignage simple)
  - [ ] Scénario 2 (témoignage avec possibilité de réécoute et de modification)
  - [ ] Scénario 3 (témoignage avec choix thématiques)
- [ ] Enregistrement du fichier audio
- [ ] Publication des témoignages
- [ ] Consultation des témoignages
- [ ] Nettoyage
  - [ ] Correction des fautes de frappes

---

## Utilisation de git

- Commencer par faire un fork du projet [mqlt35/PyCabine](https://github.com/mqlt35/PyCabine)
- Clonage du fork : `git clone git@github.com:Julie-b35/PyCabine.git`
- Contrôle origin du fork avec `git remote -v`. 
  - si `origine` n'y est pas, alors lancer la commande `git remote add origine URL_FORK`
- Ajouter le dépot principal du projet `git remote add upstream https://github.com/mqlt35/PyCabine`
- Récupérer les dernières info du projet `git pull upstream main`
- Créer une nouvelle branches (local) `git checkout -b develop`
  - La commande `git stash`peut être utile pour *mettre de côté* vos modification sans faire de commit
  - `git stash push -u` pour inclure les fichiers non tracker.
  - L'instruction suivante `git stash show -p stash@{0} -u > modification.patch` créer un patch depuis les modification locale.

--- 

Accès à la charte : [Charte programmation de la cabine téléphonique de témoignage](https://docs.google.com/document/d/1E6yp78fg-NJzNdO4ea2fbqAL292Jvwdpw8ky-wRRURM/edit?usp=sharing)

Voir
 [Programmation d'une cabine téléphonique anglaise - cabine de témoignages](https://www.wiki-rennes.fr/Programmation_d%27une_cabine_t%C3%A9l%C3%A9phonique_anglaise_-_cabine_de_t%C3%A9moignages)