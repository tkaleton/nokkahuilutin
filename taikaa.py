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

SendInput = ctypes.windll.user32.SendInput

FSAMP = 44100
FRAME_SIZE = 1024
FRAMES_PER_FFT = 8
SAMPLES_PER_FFT = FRAME_SIZE*FRAMES_PER_FFT
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT

NOTE_NAMES = 'C TYHJA1 D VAPAA E F G A TYHJA2 A H1 H2'.split()


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
            msg = sointu
            print(msg)      
            if msg == "C":
                PressAndHoldKey(Nuotit.A, 0.1)    
            if msg == "D":
                PressAndHoldKey(Nuotit.W, 0.1)
            if msg == "E":
                PressAndHoldKey(Nuotit.S, 0.1)
            if msg == "F":
                PressAndHoldKey(Nuotit.D, 0.1)
            if msg == "VAPAA":
                PressAndHoldKey(Nuotit.L, 0.05)
            if msg == "H1":
                PressAndHoldKey(Nuotit.LEFT_CONTROL, 0.1)
            if msg == "H2":
                PressAndHoldKey(Nuotit.LEFT_SHIFT, 0.1)
        except Exception as er:
            print(er)
            print('Kaatuu kun Neuvostoliitto vuonna 1991')




from pynput.keyboard import Key, Controller
keyboard = Controller()
global juusto
juusto = [0] * 267
napit = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

paikka = 0
MONES = 0
KOHDE = 0
EDELLINEN = 0


#polkastaan uberhajautus käyntiin
def polku():
    l = 0
    for i in range(1, 3):
        for j in range(1, 7):
            for k in range(1, 7):
                if i != j and j != k:
                    juusto[(i*100) + (j*10) + k] = napit[l]
                    l += 1
                if l >= len(napit):
                    return




def lisaa(n):
    global MONES
    global KOHDE
   
    if MONES == 0:
        KOHDE += 100*n
        MONES += 1
        return 
    if MONES == 1:
        KOHDE = KOHDE + 10*n
        MONES += 1
        return
    if MONES == 2:
        KOHDE = KOHDE + n
        MONES = 0
        if KOHDE < 200 and juusto[KOHDE] != 0:
            keyboard.press(juusto[KOHDE])
            print(juusto[KOHDE])
        KOHDE = 0
        return

def hoida_nuotti(sointu):
    msg = sointu
    global EDELLINEN
    global MONES
    print(sointu)
    if EDELLINEN == msg:
        return
    EDELLINEN =  msg
    if MONES == 0 and msg != "C":
        return
    if msg == "C":
       lisaa(1)
    if msg == "D":
       lisaa(2)
    if msg == "E":
        lisaa(3)
    if msg == "F":
        lisaa(4)
    if msg == "VAPAA":
        lisaa(5)
    if msg == "H1":
        lisaa(6)

    return



