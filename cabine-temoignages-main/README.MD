Installation :

Install GPIO lib :
> pip install RPi.GPIO 
or 
> pip install requirements.txt

Possible to simulate running code in not Raspberry platform (Mac, PC, ...) -- tested on MacOs
- GPIO is replaced by a similar mock library at runtime (and print's)
- GPIO input is replaced by keyboard

Audio play/record depends on external command line processes :
- arecord/aplay (ALSA) on linux
- sox (SOundeXchange) on macos


** sox

> apt-get install sox

https://gist.github.com/ideoforms/d64143e2bad16b18de6e97b91de494fd

** aplay/arecord :
https://linux.die.net/man/1/arecord

List input/output devices :
- aplay -L
- arecord -L

Update: aplay and arecord are in the 'alsa-utils' package. To install:
sudo apt install alsa-utils


Alternative arecord ?
https://forums.raspberrypi.com/viewtopic.php?t=336462

HostAPD
https://github.com/RaspAP/raspap-webgui