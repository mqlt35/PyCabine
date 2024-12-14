#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Déclancher une erreur si le script est exécuté directement.
if __name__ == "__main__" : 
    raise Exception("Ce scripte n'est pas exécutable.")

from enum import Enum
import datetime

TAUX_ECHANTILLONNAGE = 44100
class ChoicePublication(Enum):
    INTERNET = 1
    PRIVER = 2

class Enregistrement():    
    # Attribut de classe pour stocker l'unique instance
    _instance = None

    def __new__(self, *args, **kwargs):
        # Vérifie si une instance existe déjà
        # merci Chat GPT
        if not self._instance:
            self._instance = super(Enregistrement, self).__new__(self, *args, **kwargs)
            pass
        return self._instance
    def __init__(self): # A initialiser qu'une seule fois.
        if not hasattr(self, "_initialized"):
            from Cabine.Utils import Utils
            from Cabine.Factory import Factory
            self._initialized = True
            self.directoryVocalMsg = Utils.getWorkDir() + "/upload/"
            self.saveMp3File = None
            self.saveWaveFile = None
            self.Combi = Factory().getClass("Combinee")

    def setFile(self, choice_publication: ChoicePublication = ChoicePublication.INTERNET):
        curent_time = datetime.datetime.now()
        tab_save_file = [
            self.directoryVocalMsg,
            choice_publication.value,
            curent_time.day,
            curent_time.month,
            curent_time.year,
            curent_time.hour,
            curent_time.minute,
            curent_time.second
        ]
        self.saveWaveFile = "%s%s_%s-%s-%s_%s-%s-%s.wav" % tuple(tab_save_file)
        self.saveMp3File = "%s%s_%s-%s-%s_%s-%s-%s.mp3" % tuple(tab_save_file)

    def saveVocalMsg(self):
        print("saveVocalMsg : Enregistrement en cours.")
        print (self.saveWaveFile)
        import wave
        import sounddevice as sd
        from time import sleep
        try:
            with wave.open(self.saveWaveFile, 'wb') as fichier_wave:
                fichier_wave.setnchannels(1)
                fichier_wave.setsampwidth(2)
                fichier_wave.setframerate(TAUX_ECHANTILLONNAGE)
                # Démarrage de l'enregistrement en streaming
                def callback(indata, frames, time, status):
                    if status:
                        print(f"Statut : {status}")
                    #audio.append(indata.copy())
                    fichier_wave.writeframes(indata.tobytes())
                #print(self.Combi)
                with sd.InputStream(
                    samplerate=TAUX_ECHANTILLONNAGE,
                    channels=1,
                    dtype='int16',
                    callback=callback
                ):
                    while True:
                        sleep(0.1) # en prévention surchage CPU.
                        #print(self.Combi)
                        if self.Combi.combiRaccrocher():
                            break
                    #while GPIO.input(HOOK_PIN) == GPIO.HIGH:
                    #    time.sleep(0.1)
            print(f"Enregistrement terminé. Fichier enregistré sous {self.saveWaveFile}")
        except Exception as e:
            print(f"Erreur pendant l'enregistrement : {e}")
        finally:
            print("saveVocalMsg : Fin de l'enregistrement.")
            self.converteWaveToMp3()

    def converteWaveToMp3(self):
        from pydub import AudioSegment
        try:
            audio = AudioSegment.from_wav(self.saveWaveFile)
            audio.export(self.saveMp3File, format='mp3')
        except Exception as e:
            print(f"Erreur pendant la conversion wav --> mp3 : {e}")
        finally:
            #Supprier fichier wave
            print("converteWaveToMp3 : conversion wav --> mp3 effectué avec succès.")
            self.deleteFileWave()
            pass

    def deleteFileWave(self):
        from pathlib import Path
        file_path = Path(self.saveWaveFile)
        try:
            file_path.unlink()
            print(f"Le fichier {self.saveWaveFile} à bien été supprimé.")
        except FileNotFoundError as e: 
            print(f"{self.saveWaveFile} : n'existe pas. : {e}")
        except PermissionError as e:
            print(f"Permission refusée : {self.saveWaveFile} : {e}")
        except Exception as e:
            print(f"Un erreur est survenue : {e}")

    def __getattr__(self, name):
        if name == "ChoicePublication":
            return ChoicePublication
        elif name == "_initialized":
            # Sans déclancher cette erreur et en retournant None
            # hasattr dans __init__ pète les plomb.
            raise AttributeError("L'arguement existe pas.")
        # Intercepte les attributs inexistantsy
        print(f"__getattr__ appelé pour : {name}")
    
        return None