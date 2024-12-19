notes 21 novembre (Yannick)

- j'ai créé un petit programme (clavier3.py) qui utilisait des 
   GPIO.add_event_detect
J'obtenais : "RuntimeError: Failed to add edge detection"
https://stackoverflow.com/questions/75542224/runtimeerror-failed-to-add-edge-detection-on-raspberrypi

Cela 
> sudo apt --fix-broken install
> sudo apt remove python3-rpi.gpio
> sudo apt install python3-rpi-lgpio

Sur venv (après source venv/bin/activate)
> pip install rpi-lgpio
> python clavier3.py 
> python clavier.py 
