import numpy as np
import pygame
import time
from pad4pi import rpi_gpio
import RPi.GPIO as GPIO

# Initialisation de pygame.mixer
pygame.mixer.init(frequency=44100, size=-16, channels=1)

# Fréquences DTMF (Hz)
DTMF_FREQS = {
    1: (697, 1209),
    2: (697, 1336),
    3: (697, 1477),
    4: (770, 1209),
    5: (770, 1336),
    6: (770, 1477),
    7: (852, 1209),
    8: (852, 1336),
    9: (852, 1477),
    "*": (941, 1209),
    0: (941, 1336),
    "#": (941, 1477),
}

# Générer un son pour une combinaison de fréquences
def generate_dtmf(frequencies, duration=0.2, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = sum(np.sin(2 * np.pi * f * t) for f in frequencies)
    wave = (wave * 32767 / np.max(np.abs(wave))).astype(np.int16)  # Normaliser
    return pygame.sndarray.make_sound(wave)

# Associer chaque touche à un son
dtmf_sounds = {key: generate_dtmf(freqs) for key, freqs in DTMF_FREQS.items()}

# Jouer un son pour une touche
def play_dtmf(key):
    if key in dtmf_sounds:
        print(f"Jouer le son pour la touche : {key}")
        sound = dtmf_sounds[key]
        sound.play()
        while pygame.mixer.get_busy():
            time.sleep(0.05)

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

# Fonction appelée à chaque pression de touche
def handle_key_press(key):
    print(f"Touche appuyée : {key}")
    play_dtmf(key)  # Jouer la note associée à la touche

# Associer la fonction de gestion des touches au clavier
keypad.registerKeyPressHandler(handle_key_press)

try:
    print("Appuyez sur les touches du clavier matriciel (Ctrl+C pour quitter)...")
    while True:
        time.sleep(0.1)  # Attente pour éviter une utilisation CPU excessive
finally:
    print("Nettoyage et arrêt...")
    GPIO.cleanup()
    pygame.mixer.quit()
