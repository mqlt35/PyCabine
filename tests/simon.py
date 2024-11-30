import os
import random
import time
from pad4pi import rpi_gpio
import RPi.GPIO as GPIO
import pygame.midi

# Connecte MIDI Through Port-0 à FluidSynth
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

# Configuration du GPIO pour le détecteur décroché/raccroché
GPIO.setmode(GPIO.BCM)
HOOK_PIN = 17  # Remplace par le numéro réel de ton GPIO
GPIO.setup(HOOK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialisation de pygame.midi
pygame.midi.init()
player = None

try:
    player = pygame.midi.Output(0)
    player.set_instrument(0)  # Instrument MIDI (0 = Piano)

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

    # Jouer une note
    def jouer_note(note, duree=0.2):
        player.note_on(note, 127)
        time.sleep(duree)
        player.note_off(note, 127)

    # Jouer une séquence
    def jouer_sequence(sequence):
        for note in sequence:
            jouer_note(KEY_TO_NOTE[note], 0.5)
            time.sleep(0.2)  # Pause entre les notes

    # Mélodie succès/échec
    def jouer_melodie(melodie, duree=0.1, pause=0.05):
        for note in melodie:
            jouer_note(note, duree)
            time.sleep(pause)

    MELODIE_SUCCES = [76, 79, 83]  # Do5, Mi5, Sol5
    MELODIE_ECHEC = [71, 67, 60]   # Si4, Sol4, Do4

    # Jeu principal
    def simon():
        sequence = []  # Séquence générée
        niveau = 1
        joueur_index = 0

        print("Début du jeu Simon. Décrochez le combiné pour commencer !")

        def handle_key_press(key):
            nonlocal sequence, niveau, joueur_index
            print(f"Touche appuyée : {key}")
            if joueur_index < len(sequence) and key == sequence[joueur_index]:
                jouer_note(KEY_TO_NOTE[key])
                joueur_index += 1
                if joueur_index == len(sequence):  # Succès pour la séquence actuelle
                    time.sleep(1)  # Pause avant la mélodie de succès
                    jouer_melodie(MELODIE_SUCCES, duree=0.05, pause=0.03)
                    time.sleep(1)  # Pause avant la prochaine consigne
                    niveau += 1
                    jouer_simon()
            else:  # Échec
                time.sleep(1)  # Pause avant la mélodie d'échec
                jouer_melodie(MELODIE_ECHEC, duree=0.05, pause=0.03)
                sequence.clear()
                niveau = 1
                jouer_simon()

        def jouer_simon():
            nonlocal sequence, joueur_index
            joueur_index = 0
            sequence = [random.choice(list(KEY_TO_NOTE.keys())) for _ in range(niveau)]
            print(f"Séquence niveau {niveau} : {sequence}")
            jouer_sequence(sequence)

        keypad.registerKeyPressHandler(handle_key_press)

        try:
            while True:
                # Attendre que le combiné soit décroché
                if GPIO.input(HOOK_PIN) == GPIO.LOW:
                    print("Combiné décroché. Attente de 2 secondes avant de commencer.")
                    time.sleep(2)  # Attente de 2 secondes
                    joueur_index = 0
                    niveau = 1
                    sequence.clear()
                    jouer_simon()

                    # Boucle principale pendant que le combiné est décroché
                    while GPIO.input(HOOK_PIN) == GPIO.LOW:
                        time.sleep(0.1)  # Maintenir le jeu actif
                    print("Combiné raccroché. Réinitialisation du jeu.")
                    time.sleep(1)  # Petite pause avant de détecter un nouveau décroché

        finally:
            print("Fin de la boucle de jeu. Réinitialisation.")

    simon()

except KeyboardInterrupt:
    print("Interruption clavier détectée. Nettoyage des ressources...")
finally:
    print("Nettoyage final...")
    if player:
        del player
    pygame.midi.quit()
    GPIO.cleanup()
