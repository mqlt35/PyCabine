#!/usr/bin/env python3
#-- coding: utf-8 --
import platform

import os
import sys
import subprocess
from time import sleep
from subprocess import Popen

def record_audio_start(audio_filename, timeInSec):
    record_cmd_line = f"arecord --device=hw:1,0 --duration={timeInSec} --format S16_LE --rate 44100 -V mono -c1 {audio_filename}"
    if platform.system() != 'Linux': # not raspberry
        record_cmd_line = "sox -q -d "+audio_filename
    return subprocess.Popen([record_cmd_line], shell=True)

def record_audio_stop(proc):
    proc.terminate()
    print("Closing the recording and wait please....")

def play_audio(audio_filename):
    play_cmd_line = "aplay --device=plughw:1,0 "+audio_filename
    if platform.system() != 'Linux': # not raspberry
        play_cmd_line = "play -q "+audio_filename

    print("Listening after two seconds")
    proc = subprocess.Popen([play_cmd_line], shell=True)

if __name__ == "__main__":

    audio_filename = "recording.wav"

    print("Recording now...")
    timeInSec = 5
    proc = record_audio_start(audio_filename, timeInSec)
    sleep(timeInSec)
    record_audio_stop(proc)

    sleep(1)
    print("Listening now...")
    sleep(1)

    play_audio(audio_filename)

    print("finished")