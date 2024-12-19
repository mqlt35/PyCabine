14 novembre 2024

Fin de soudure et cablage du clavier matriciel.
J'essaye de le faire fonctionner avec la bibliothèque pad4pi https://pypi.org/project/pad4pi/

ça ne fonctionne pas. Pendant l'install de pad4pi, indication :
----
DEPRECATION: RPi.GPIO is being installed using the legacy 'setup.py install' method, because it does not have a 'pyproject.toml' and the 'wheel' package is not installed. pip 23.1 will enforce this behaviour change. A possible replacement is to enable the '--use-pep517' option. Discussion can be found at https://github.com/pypa/pip/issues/8559
  Running setup.py install for RPi.GPIO ... done
Successfully installed RPi.GPIO-0.7.1 pad4pi-1.1.5
----

J'ai vu successfully, je me suis dit que ça passait quand même...
Mais l'exécution du fichier renvoie 
----
GPIO.add_event_detect(self._row_pins[i], GPIO.FALLING, callback=self._onKeyPress, bouncetime=DEFAULT_DEBOUNCE_TIME)
RuntimeError: Failed to add edge detection
----

Florent passe par là et dit que ça vient d'un conflit de librairie GPIO.
Il tente : 
sudo apt remove python3-rpi.gpio
sudo apt update
sudo apt install python3-rpi-lgpio (estimant que pour pouvoir gérer la bibliothèque pad4pi, il faut une bibliothèque GPIO qui gère l'envoi? ou la réception? de qqch ?)
... mais ça déconne : 
----
nmet dependencies. Try 'apt --fix-broken install' with no packages (or specify a solution)
----
il fait : 
sudo apt --fix-broken install
sudo apt remove python3-rpi.gpio
sudo apt --fix-broken install