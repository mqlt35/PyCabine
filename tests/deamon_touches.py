import time
import RPi.GPIO as GPIO
from threading import Thread
print("ici")
class Keypad:
    def __init__(self, row_pins, col_pins):
        self.row_pins = row_pins
        self.col_pins = col_pins
        self.keypad = [
            [1, 2, 3],   # Correspondance des touches
            [4, 5, 6],
            [7, 8, 9],
            ["*", 0, "#"]
        ]
        self.running = True
        self.pressed_keys = set()  # Garder une trace des touches actuellement pressées
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BCM)
        self.polling_thread = None

    def setup(self):
        # Configurer les lignes comme INPUT (avec résistance pull-up)
        for pin in self.row_pins:
            self.GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Configurer les colonnes comme OUTPUT (initialement HIGH)
        for pin in self.col_pins:
            self.GPIO.setup(pin, GPIO.OUT)
            self.GPIO.output(pin, GPIO.HIGH)

    def scan_keys(self):
        """Scanner les touches et détecter les pressions et relâchements."""
        for col_index, col_pin in enumerate(self.col_pins):
            # Activer une colonne (LOW) et désactiver les autres (HIGH)
            self.GPIO.output(col_pin, GPIO.LOW)
            time.sleep(0.01)  # Pause pour stabilisation

            for row_index, row_pin in enumerate(self.row_pins):
                key = self.keypad[row_index][col_index]
                if not self.GPIO.input(row_pin):  # Si la ligne est activée (LOW)
                    if key not in self.pressed_keys:  # Nouvelle pression
                        self.pressed_keys.add(key)
                        self.on_key_press(key)
                else:  # Si la ligne est désactivée (HIGH)
                    if key in self.pressed_keys:  # Clé précédemment pressée
                        self.pressed_keys.remove(key)
                        self.on_key_release(key)

            # Désactiver la colonne actuelle
            self.GPIO.output(col_pin, GPIO.HIGH)

    def start_polling(self):
        """Démarrer le thread de polling des touches."""
        print("polling_thread", self.polling_thread, self.polling_thread.is_alive())
        if not self.polling_thread or not self.polling_thread.is_alive():
            self.polling_thread = Thread(target=self.poll_keys)
            self.polling_thread.start()

    def poll_keys(self):
        """Boucle de détection des touches."""
        while self.running:
            self.scan_keys()
            time.sleep(0.01)  # Pause entre les scans

    def stop(self):
        """Arrêter le polling et nettoyer les GPIO."""
        self.running = False
        if self.polling_thread:
            self.polling_thread.join()  # Attendre que le thread termine proprement
        self.GPIO.cleanup()

    def on_key_press(self, key):
        """Callback pour l'appui sur une touche."""
        print(f"Touche pressée : {key}")

    def on_key_release(self, key):
        """Callback pour le relâchement d'une touche."""
        print(f"Touche relâchée : {key}")


# Configuration des broches
ROW_PINS = [5, 6, 13, 19]  # Numérotation BCM
COL_PINS = [16, 20, 21]    # Numérotation BCM

def main():
    try:
        keypad = Keypad(ROW_PINS, COL_PINS)
        keypad.setup()
        keypad.start_polling()

        # Rester en attente d'un arrêt manuel
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nArrêt du programme.")
        keypad.stop() 

if __name__ == "__main__":
    main()
