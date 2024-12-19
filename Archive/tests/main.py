#!/usr/bin/env python3
#-- coding: utf-8 --
import platform
from os.path import exists
import time
from threading import Thread

from enum import Enum

from simple_audio_play_record import play_record

# GPIO and cross-platform development
if platform.system()=='Linux': # raspberry
 	from RPi import GPIO
else: # macos or stg else...
    import dummy_gpio_sim.dummygpiosim as GPIO

GPIO.setwarnings(False) # on désactive les messages d'alerte
GPIO.setmode(GPIO.BOARD) # définit le mode de numérotation (Board)
# ref doc : https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
PIN_COMBINE = 21

def enregistrementThreadFn():
    Enregistrement()
recording_thread = Thread(target=enregistrementThreadFn)

class Etat(Enum):
    INITIALISATION = 1
    PRETE = 2
    ANNONCE = 3
    ENREGISTREMENT = 4
    ARRET_ENREGISTREMENT = 5

etat = Etat.INITIALISATION

def DecrochageRaccrochageCombine(e):
    if GPIO.input(PIN_COMBINE):
        DecrochageCombine()
    else:
        RaccrochageCombine()

def main():
    global etat

    print("Initialisation de la cabine de témoignage....")
    GPIO.setup(PIN_COMBINE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(PIN_COMBINE, GPIO.BOTH, callback=DecrochageRaccrochageCombine, bouncetime=1000)

    etat = Etat.PRETE

    print("La cabine de témoignage est disponible.")

    # boucle infinie
    while(True):
        if platform.system()=='Linux': # raspberry
            time.sleep(1) # infini
        else:
            # debug on PC/Mac : use text inputs to simulate events from gpio pins
            command = input("> ").upper()
            if command == "D":
                DecrochageCombine()
            elif command == "R":
                RaccrochageCombine() 
            elif command == "Q": # quit
                break

def DecrochageCombine():
    print("Decrochage Combiné")
    global etat, recording_thread
    if etat == Etat.INITIALISATION :
        # TODO Annonce Cabine en cours d'initialisation
        print("Annonce Cabine en cours d'initialisation")
        
        # next : 
        etat = Etat.ANNONCE
        pass
    else:
        etat = Etat.ANNONCE
        # TODO Annonce pré-enregistrement
        print("Annonce pré-enregistrement")
        Annonce()

def RaccrochageCombine():
    global etat
    print("Raccrochage Combiné");
    if (etat == Etat.INITIALISATION) or (etat == Etat.PRETE):
        print("ignore")
        return

    if (etat == Etat.ENREGISTREMENT):
        etat = Etat.ARRET_ENREGISTREMENT
        recording_thread.join()
        print("Arrêt de l'enregistrement...")

    if (etat == Etat.ANNONCE):
        # //TODO stopper l'annonce
        print("stopper l'annonce")

    etat = Etat.PRETE

def Annonce():
    global recording_thread
    play_record.play_audio("annonce.wav")
    time.sleep(7)

    # démarrage enregistrement
    recording_thread = Thread(target=enregistrementThreadFn)
    recording_thread.start()

def Enregistrement():
    global etat
    etat = Etat.ENREGISTREMENT

    # # increment recording files to a new (next not existing file name with number)
    # i = 0
    # while exists(f"enregistrements/temoignage-{i:03}.wav"):
    #     i += 1
    # proc = play_record.record_audio_start(f"enregistrements/temoignage-{i:03}.wav", 10)

    # while etat == Etat.ENREGISTREMENT:
    #     # TODO faire l'engistrement
    #     print("Enregistrement en cours")
    #     time.sleep(1)

    # play_record.record_audio_stop(proc)

    # print("Fin enregistrement")

    play_record.play_audio("appel18juin.wav")
    time.sleep(10)

    # //TODO sauvegarder l'engistrement

if __name__ == "__main__":
    main()