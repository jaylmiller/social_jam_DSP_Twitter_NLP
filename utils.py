"""
Utility functions
"""

import numpy as np
import scipy.signal as signal
from global_vars import *


def decode(data):
    return np.frombuffer(data, dtype=np.float32)


def encode(signal):
    return signal.astype(np.float32).tostring()

pitches = np.array([55.00,   58.27,   61.74,
  65.41,   69.30,   73.42,   77.78,   82.41,   87.31,   92.50,   98.00,   103.8,   110.0,   116.5,   123.5,
   130.8,   138.6,   146.8,   155.6,   164.8,   174.6,   185.0,   196.0,   207.7,   220.0,   233.1,   246.9,
   261.6,   277.2,   293.7,   311.1,   329.6,   349.2,   370.0,   392.0,   415.3,   440.0,   466.2,   493.9,
   523.3,   554.4,   587.3,   622.3,   659.3,   698.5,   740.0,   784.0,   830.6,   880.0,   932.3,   987.8,
   1047,    1109,    1175,    1245,    1319,    1397,    1480], dtype=np.float32)

pitch_ratios = {'minor_third': 6.0/5.0, 
                'major_third': 5.0/4.0,
                'perfect_fourth': 4.0/3.0,
                'tritone': np.sqrt(2),
                'perfect_fifth': 3.0/2.0,
                'octave': 2.0/1.0}


def pitch_detect_fft_bins(signal):
    dft = np.fft.rfft(signal, BUFFER_SIZE)
    dft = np.absolute(dft)
    max_index = np.argmax(dft)
    fund_freq = np.fft.rfftfreq(BUFFER_SIZE, 1.0/float(RATE))[max_index]
    index = (np.abs(pitches - fund_freq)).argmin()
    return pitches[index]

def pitch_detect_zero_crossing(signal):
    diff_threshold = 50
    zero_crossings = np.where(np.diff(np.signbit(signal)))[0]
    diffs = np.ediff1d(zero_crossings)
    diffs = [d for d in diffs if d > diff_threshold]
    avg = np.mean(diffs)
    return float(RATE)/avg/2.0

""" Speed up sound change speed """ 
def speed_up(signal, factor):
    indices = np.round( np.arange(0, len(signal), factor) )
    indices = indices[indices < len(signal)].astype(int)
    return signal[indices.astype(int)]


"""
pitch shift a signal but keep it the same length.
note interval must be in pitch ratios dict
"""
def pitch_shift(signal, interval):
    pitch = pitch_detect_zero_crossing(signal)
    new_pitch = pitch*pitch_ratios['interval']

    return 


    