import os
from pad4pi import rpi_gpio
import RPi.GPIO as GPIO
import pygame.midi
import time

# Connecte MIDI Through Port-0 à FluidSynth 
# - attention, il semble que cette commande ne fonctionne pas quand on lance le fichier depuis venv.  
# Dans ce cas, exécuter aconnect 14:0 128:0 dans le terminal avant de lancer clavier_notes.py
os.system("aconnect 14:0 128:0")

# Configuration du clavier matriciel
KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

ROW_PINS = [5, 6, 13, 19]  # Numérotation BCM
COL_PINS = [16, 20, 21]    # Numérotation BCM

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

# Initialisation de pygame.midi
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

player = pygame.midi.Output(0)  # Assurez-vous que Midi Through Port-0 est configuré
player.set_instrument(0)        # Instrument MIDI (0 = Piano)

# Associer chaque touche à une note MIDI
KEY_TO_NOTE = {
    1: 60,  # Do (C4)
    2: 62,  # Ré (D4)
    3: 64,  # Mi (E4)
    4: 65,  # Fa (F4)
    5: 67,  # Sol (G4)
    6: 69,  # La (A4)
    7: 71,  # Si (B4)
    8: 72,  # Do (C5)
    9: 74,  # Ré (D5)
    0: 76   # Mi (E5)
}

# Fonction pour jouer une note
def jouer_note(note):
    player.note_on(note, 127)  # Jouer la note avec une vélocité de 127
    time.sleep(0.5)            # Durée de la note
    player.note_off(note, 127) # Arrêter la note

# Fonction appelée à chaque pression de touche
def handle_key_press(key):
    print(f"Touche appuyée : {key}")
    if key in KEY_TO_NOTE:
        jouer_note(KEY_TO_NOTE[key])  # Jouer la note associée

# Associer la fonction de gestion des touches au clavier
keypad.registerKeyPressHandler(handle_key_press)

try:
    while True:
        value = input("(q pour quitter) > ")
        if value == "q":
            break
finally:
    print("Nettoyage et arrêt...")
    GPIO.cleanup()
    del player
    pygame.midi.quit()
