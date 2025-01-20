#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")



#import pygame
import time


# Initialisation de pygame.mixer
#pygame.mixer.init(frequency=44100, size=-16, channels=1)

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


DURATION = 10.0

# Création d'une classe Touches qui renvoie le numéro de la touche appuyée et qui génère les fréquences associées (biiip)
class Touches :
	def __init__(self, api):
		# Associer la fonction de gestion des touches au clavier
		self.__api = api
		self.pressed_button = None
		self._load = False

	def configure(self):
		self.__mixer = self.__api.getTools_Mixer()
		self.__pad = self.__api.getTools_Pad()

	def pre_run(self):
		print("Touches : Initialisation du clavier matriciel : pre_run")
		# Initialisation du clavier matriciel
		self.__pad.init_keypad(KEYPAD, ROW_PINS, COL_PINS)
		self.__dtmf_sounds = {key: self.generate_dtmf(freqs, DURATION) for key, freqs in DTMF_FREQS.items()}
	# Fonction appelée à chaque pression de touche
	def handle_key_press(self,key):
		print(f"Touche appuyée : {key}")
		self.pressed_button = key
		self.play_dtmf(key)  # Jouer la note associée à la touche

	def handle_release_key(self, key):
		print(f"Touche relaché : {key}")
		self.stop_dtmf(key)

    # Générer un son pour une combinaison de fréquences
	def generate_dtmf(self,frequencies, duration=5.0, sample_rate=44100):
		import numpy as np
		t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
		wave = sum(np.sin(2 * np.pi * f * t) for f in frequencies)
		wave = (wave * 32767 / np.max(np.abs(wave))).astype(np.int16)  # Normaliser
		return self.__mixer.make_sound(wave)
		#return pygame.sndarray.make_sound(wave)

	# Jouer un son pour une touche
	def play_dtmf(self,key):			    
		# Associer chaque touche à un son
		
		if key in self.__dtmf_sounds:
			sound = self.__dtmf_sounds[key]
			sound.play()

	def stop_dtmf(self, key):
		if key in self.__dtmf_sounds:
			sound = self.__dtmf_sounds[key]
			sound.stop()

	def clean(self):
		#Nettoyage
		self.__pad.cleanup()
		self.__mixer.clean()

	def load(self):
		if self._load == False:
			self.__pad.registerKeyPressHandler(self.handle_release_key, self.handle_key_press)
			self._load = True

	def unload(self):
		if self._load == True:
			self.__pad.unregisterKeyPressHandler(self.handle_release_key, self.handle_key_press)
			self._load = False

	def getButtonPressed(self):
		if not self._load:
			raise Exception("Touches.py : Les touches du clavier doivent être d'abord Charger.")
		
		save_pressed_button = self.pressed_button
		self.pressed_button = None
		return save_pressed_button 

def init(api):
    global _
    _ = api._
    return Touches(api)