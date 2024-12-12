import os
import pygame.midi
import time

# Connecte MIDI Through Port-0 à FluidSynth
os.system("aconnect 14:0 128:0")

# Initialisation
pygame.midi.init()

# Liste des périphériques MIDI
for i in range(pygame.midi.get_count()):
    info = pygame.midi.get_device_info(i)
    print(f"ID: {i}, Nom: {info[1].decode()}, Sortie: {info[3]}")


# Sélection de FluidSynth comme sortie MIDI
fluid_device_id = 0

if fluid_device_id is None:
    print("Erreur : FluidSynth n'est pas détecté. Assurez-vous qu'il est lancé.")
    exit(1)

player = pygame.midi.Output(fluid_device_id)  # Connecte à FluidSynth
player.set_instrument(0)  # Instrument MIDI (0 = Piano)

# Fonction pour jouer une note
def jouer_note(note, duration=1):
    """
    Joue une note MIDI.
    - note : entier (hauteur, ex. 60 pour le Do central)
    - duration : durée en secondes
    """
    player.note_on(note, 127)  # Volume de 0 à 127
    time.sleep(duration)
    player.note_off(note, 127)

# Exemple : jouer Do, Mi, Sol
jouer_note(60, 0.5)  # Do (C4)
jouer_note(64, 0.5)  # Mi (E4)
jouer_note(67, 0.5)  # Sol (G4)

# Nettoyage
del player
pygame.midi.quit()
