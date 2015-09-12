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
    order = 50
    
    def __init__(self, cut_off_freq=500):
        self.a = [1.0]
        self.b = 0.
        self.set_params(cut_off_freq=cut_off_freq)


    def get_effected_signal(self, sig):
        return signal.lfilter(self.b, self.a, sig)


    def set_params(self, **kwargs):
        f = kwargs['cut_off_freq']
        self.b = signal.firwin(LowpassFilter.order, cutoff = f, window = "hamming",
                               nyq=RATE*.5)




ALL_FX = [LowpassFilter]