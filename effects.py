import numpy as np
import scipy.signal as signal

"""
All effects must implement: 
    get_effected_signal(signal)
    set_params(**kwargs)
"""


class LowpassFilter(object):

    pass_band_loss = 2 # max loss in passing band (dB)
    stop_band_loss = 30 # min loss in stopping band (dB)
    
    
    def __init__(cut_off_freq):
        this.a = 0.
        this.b = 0.
        this.set_cut_off(cut_off_freq)


    def get_effected_signal(signal):
        return signal.lfilter(this.b, this.a, signal)


    def set_params(**kwargs):
        normalized_pass = kwargs['cut_off_freq']/((RATE/1000.)*.5)
        normalized_stop = normalized_pass+.1*normalized_pass
        order, nat_freq = signal.buttord(normalized_pass, normalized_stop,
                                         pass_band_loss, stop_band_loss)
        this.b, this.a = signal.butter(order, nat_freq, btype='low')