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


"""
Detect pitch by matching the highest amplitude
frequenct in the DFT with the pitch for a musical note.
"""
def pitch_detect_fft_bins(signal):
    dft = np.fft.rfft(signal, BUFFER_SIZE)
    dft = np.absolute(dft)
    max_index = np.argmax(dft)
    fund_freq = np.fft.rfftfreq(BUFFER_SIZE, 1.0/float(RATE))[max_index]
    index = (np.abs(pitches - fund_freq)).argmin()
    return pitches[index]


"""
Detect pitch using zero crossing rate average and removing noise
by adding a threshold
"""
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
pitch shift a signal
note interval must be in pitch ratios dict
"""
def pitch_shift(signal, interval):
    pitch = pitch_detect_zero_crossing(signal)
    new_signal = speed_up(signal, pitch_ratios[interval])
    return np.append(new_signal, 
    				  np.zeros(len(signal)-len(new_signal)))


    