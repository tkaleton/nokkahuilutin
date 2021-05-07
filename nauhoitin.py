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
import nuotit

######################################################################
# Feel free to play with these numbers. Might want to change NOTE_MIN
# and NOTE_MAX especially for guitar/bass. Probably want to keep
# FRAME_SIZE and FRAMES_PER_FFT to be powers of two.

NOTE_MIN = 10       # C4
NOTE_MAX = 100      # A4
FSAMP = 44100       # Sampling frequency in Hz
FRAME_SIZE = 2048   # How many samples per frame?
FRAMES_PER_FFT = 16 # FFT takes average across how many frames?
VOLUME_TRESHOLD = 1
NUM_FRAMES = 0

SendInput = ctypes.windll.user32.SendInput


######################################################################
# Derived quantities from constants above. Note that as
# SAMPLES_PER_FFT goes up, the frequency step size decreases (so
# resolution increases); however, it will incur more delay to process
# new sounds.

SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT

IMIN = max(0, int(np.floor(note_to_fftbin(NOTE_MIN-1))))
IMAX = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX+1))))
WINDOW = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))
BUF = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)

NOTE_NAMES = 'ETEEN TAAKSE VASEN AMMU KYYKKYYN HYPPÄÄ TYHJA OIKEA RELOAD 2 3 4'.split()


def PressKeyPynput(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKeyPynput(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def PressAndHoldKey(hexKeyCode, seconds):
    PressKeyPynput(hexKeyCode)
    time.sleep(seconds)
    ReleaseKeyPynput(hexKeyCode)

def freq_to_number(f): 
    return 69 + 12*np.log2(f/440.0)

def number_to_freq(n): 
    return 440 * 2.0**((n-69)/12.0)

def note_name(n): 
    return NOTE_NAMES[n % 12]

def note_to_fftbin(n): 
    return number_to_freq(n)/FREQ_STEP

def rms(data):
    count = len(data)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, data )
    sum_squares = 0.0
    
    for sample in shorts:
        n = sample * (1.0/FRAME_SIZE)
        sum_squares += n*n
    
    return math.sqrt( sum_squares / count )

def laheta_input(sointu=None):
    if sointu is None:
        return
    else:
        try:  
            msg = sointu.upper()
            
            if msg == "VASEN":
                print(msg)
                #PressAndHoldKey(A, 2)

            if msg == "OIKEA":
                print(msg)
                #PressAndHoldKey(D, 2)

            if msg == "ETEEN":
                print(msg)
                #ReleaseKeyPynput(S) #release brake key first
                #PressKeyPynput(W) #start permanently driving

            if msg == "TAAKSE":
                print(msg)
                #ReleaseKeyPynput(W) #release drive key first
                #PressKeyPynput(S) #start permanently reversing

            if msg == "HYPPAA":
                print(msg)
                #PressAndHoldKey(SPACE, 0.7)

            if msg == "KYYKKYYN":
                print(msg)
                
            if msg == "RELOAD":
                print(msg)
                
            if msg == "AMMU":
                print(msg)
                #mouse.press(Button.left)
                    #time.sleep(1)
                    #mouse.release(Button.left)
            if msg == "1":
                print(msg)
            if msg == "2":
                print(msg)
            if msg == "3":
                print(msg)           
            if msg == "4":
                print(msg)
                
        except:
            print('Kaatuu kuin Neuvostoliitto vuonna 1991')



   

stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                channels=1,
                                rate=FSAMP,
                                input=True,
                                frames_per_buffer=FRAME_SIZE)

stream.start_stream()


print("Nyt huilutellaan!")
while stream.is_active():

    BUF[:-FRAME_SIZE] = BUF[FRAME_SIZE:]
    BUF[-FRAME_SIZE:] = np.fromstring(stream.read(FRAME_SIZE), np.int16)

    rms_value = rms(stream.read(FRAME_SIZE))
    if rms_value > VOLUME_TRESHOLD:

        fft = np.fft.rfft(BUF * WINDOW)
        freq = (np.abs(fft[IMIN:IMAX]).argmax() + IMIN) * FREQ_STEP

        n = freq_to_number(freq)
        note = int(round(n))

        NUM_FRAMES += 1

        if NUM_FRAMES >= FRAMES_PER_FFT:
            laheta_input(note_name(note))