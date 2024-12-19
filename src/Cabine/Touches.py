#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

# Configuration du clavier matriciel
KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

NAME_KEYPAD = {
	1 : KEYPAD[0][0], 4 : KEYPAD[1][0], 7 : KEYPAD[2][0], "*" : KEYPAD[3][0],
	2 : KEYPAD[0][1], 5 : KEYPAD[1][1], 8 : KEYPAD[2][1],  0  : KEYPAD[3][1],
	3 : KEYPAD[0][2], 6 : KEYPAD[1][2], 9 : KEYPAD[2][2], "#" : KEYPAD[3][2]
}

ROW_PINS = [5, 6, 13, 19]  # Numérotation BCM
COL_PINS = [16, 20, 21]    # Numérotation BCM




# Création d'une classe Touches qui renvoie le numéro de la touche appuyée et qui génère les fréquences associées (biiip)
class Touches :
	def __init__(self):
		# Associer la fonction de gestion des touches au clavier
		factory = rpi_gpio.KeypadFactory()
		self.keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
		#self.load()
		self.pressed_button = None
		self._load = False

	# Fonction appelée à chaque pression de touche
	def handle_key_press(self,key):
		#print(f"Touche appuyée : {key}")
		self.pressed_button = key
		self.play_dtmf(key)  # Jouer la note associée à la touche


    # Générer un son pour une combinaison de fréquences
	def generate_dtmf(self,frequencies, duration=0.2, sample_rate=44100):
		t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
		wave = sum(np.sin(2 * np.pi * f * t) for f in frequencies)
		wave = (wave * 32767 / np.max(np.abs(wave))).astype(np.int16)  # Normaliser
		return pygame.sndarray.make_sound(wave)

	# Jouer un son pour une touche
	def play_dtmf(self,key):			    
		# Associer chaque touche à un son
		dtmf_sounds = {key: self.generate_dtmf(freqs) for key, freqs in DTMF_FREQS.items()}
		if key in dtmf_sounds:
			#print(f"Jouer le son pour la touche : {key}")
			sound = dtmf_sounds[key]
			sound.play()
			while pygame.mixer.get_busy():
				time.sleep(0.05)
	def clean(self):
		#Nettoyage
		GPIO.cleanup()
		pygame.mixer.quit()	

	def load(self):
		if self._load == False:
			self.keypad.registerKeyPressHandler(self.handle_key_press)	
			self._load = True

	def unload(self):
		if self._load == True:
			self.keypad.unregisterKeyPressHandler(self.handle_key_press)
			self._load = False

	def getButtonPressed(self):
		if not self._load:
			raise Exception("Touches.py : Les touches du clavier doivent être d'abord Charger.")
		
		save_pressed_button = self.pressed_button
		self.pressed_button = None
		return save_pressed_button 

if __name__ == "__main__" :
	clsTouche = Touches()
	print(clsTouche.getButtonPressed())

