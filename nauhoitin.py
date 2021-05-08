import numpy as np
import pyaudio
import struct
import math
import time
import subprocess
import ctypes
import random
import string
import pyautogui
import pynput
from pynput.mouse import Button, Controller
from nuotit import Nuotit
from taikaa import *

NOTE_MIN = 10
NOTE_MAX = 100
FSAMP = 44100
FRAME_SIZE = 1024
FRAMES_PER_FFT = 8
VOLUME_TRESHOLD = 0.3
SAMPLES_PER_FFT = FRAME_SIZE*FRAMES_PER_FFT
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT


imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))
window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))
buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
num_frames = 0

polku()

stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                channels=1,
                                rate=FSAMP,
                                input=True,
                                frames_per_buffer=FRAME_SIZE)

stream.start_stream()


print("Nyt huilutellaan!")
while stream.is_active():

    buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
    buf[-FRAME_SIZE:] = np.frombuffer(stream.read(FRAME_SIZE), np.int16)

    rms_value = rms(stream.read(FRAME_SIZE))

    if rms_value > VOLUME_TRESHOLD:
        fft = np.fft.rfft(buf * window)
        freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP

        n = freq_to_number(freq)
        note = int(round(n))

        num_frames += 1

        if num_frames >= FRAMES_PER_FFT:
            # Peli moduuli
            laheta_input(note_name(note))
            # Kirjoitus mooduuli
            #hoida_nuotti(note_name(note))
