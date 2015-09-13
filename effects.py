import numpy as np
import scipy.signal as signal
from global_vars import *

"""
All effects must implement: 
    get_effected_signal(signal)
    set_params(**kwargs)
"""


class LowpassFilter(object):

    pass_band_loss = 1  # max loss in passing band (dB)
    stop_band_loss = 30 # min loss in stopping band (dB)
    
    def __init__(self, cut_off_freq=1000):
        self.a = 0.
        self.b = 0.
        self.set_params(cut_off_freq=cut_off_freq)


    def get_effected_signal(self, sig):
        return signal.lfilter(self.b, self.a, sig)


    def set_params(self, **kwargs):
        f = kwargs['cut_off_freq']
        normalized_pass = f/(RATE*.5)
        normalized_stop = (f+.3*f)/(RATE*.5)
        (self.b, self.a) = signal.iirdesign(normalized_pass, normalized_stop, 
                                            LowpassFilter.pass_band_loss, 
                                            LowpassFilter.stop_band_loss)


class Reverb(object):

    def __init__(self, delay=256, decay=5):
        self.delay = delay
        self.decay = decay

    def get_effected_signal(self, signal):
        rev = np.roll(signal, self.delay) * self.decay
        rev[0 : self.delay - 1] = 0
        return signal + rev


class Tremolo(object):

    def __init__(self, freq=2.5, intensity=1.0):
        self.length = RATE/freq
        factor = float(freq) * np.pi * 2.0 / float(RATE)
        self.sin_wave = np.sin(np.arange(self.length) * factor)
        print self.sin_wave
        self.sin_wave = np.absolute(self.sin_wave)
        self.sin_wave = self.sin_wave*intensity
        self.sin_wave = self.sin_wave + (1-intensity)

    def get_effected_signal(self, signal):
        w = np.array(self.sin_wave)
        while len(w) < len(signal):
            w = np.append(w, self.sin_wave)
        self.sin_wave = np.roll(self.sin_wave, len(w)-len(signal))
        w = w[0:len(signal)]
        print w
        return signal*w

ALL_FX = [LowpassFilter, Reverb, Tremolo]
