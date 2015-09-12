import numpy as np
import scipy.signal as signal
from global_vars import *

"""
All effects must implement: 
    get_effected_signal(signal)
    set_params(**kwargs)
"""


class LowpassFilter(object):

    pass_band_loss = 1 # max loss in passing band (dB)
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

    def __init__(self):
        self.delay = 1000
        self.decay = 1

    def get_effected_signal(self, signal):
        rev = np.roll(signal, self.delay) * self.decay
        rev[0 : self.delay - 1] = 0
        return signal + rev



ALL_FX = [LowpassFilter, Reverb]