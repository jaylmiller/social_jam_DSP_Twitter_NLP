import time
import numpy as np
import scipy.signal as signal
import scipy.io.wavfile
import scipy.stats as stats
from global_vars import *
from utils import *

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


class Wah(object):

	pass_band_loss = 1  # max loss in passing band (dB)
	stop_band_loss = 30 # min loss in stopping band (dB)
	
	def __init__(self, cut_off_freq=600, osc_freq=2):
		self.it = 0
		self.set_params(cut_off_freq=cut_off_freq, osc_freq=osc_freq)


	def get_effected_signal(self, sig):
		if self.it >= 1000:
			self.it = 0
		freq = self.f + self.sin_wave[self.it]
		self.it += 1
		normalized_pass = freq/(RATE*.5)
		normalized_stop = (freq+.3*freq)/(RATE*.5)
		(a, b) = signal.iirdesign(normalized_pass, normalized_stop, 1, 30)
		out = signal.lfilter(b, a, sig)
		return out / np.max(out)


	def set_params(self, **kwargs):
		self.osc_freq = kwargs['osc_freq']
		self.f = kwargs['cut_off_freq']
		self.sin_wave = (self.f / 4) * np.sin(np.linspace(0,
			self.osc_freq * 2 * np.pi, num=1000, endpoint=True))
		self.sin_wave = np.roll(self.sin_wave, -self.it).astype(int)
		self.it = 0


class Reverb(object):

	def __init__(self, predelay=512, wet=8, decay=0.25):
		self.set_params(predelay=predelay, wet=wet, decay=decay)

	def reverb(self, signal):
		if self.iterations == self.wet:
			self.iterations = 0
			return np.zeros(BUFFER_SIZE)
		else:
			out = np.roll(signal, self.predelay // (2 ** self.iterations))
			out[0 : self.predelay] = 0
			self.iterations += 1
			out += (self.reverb(out) * self.decay)
			#print out
			return out


	def get_effected_signal(self, signal):
		return self.reverb(signal) + (signal * (self.decay / (2 ** self.wet)))

	def set_params(self, **kwargs):
		self.predelay = kwargs['predelay']
		self.wet = kwargs['wet']
		self.decay = kwargs['decay']
		self.iterations = 0


class SciFiDelay(object):

	def __init__(self, sampleDelay=512, ratio=0.75):
		self.set_params(sampleDelay=sampleDelay, ratio=ratio)

	def get_effected_signal(self, signal):
		chunk = signal[0 : self.nSamples]
		delay = np.zeros(BUFFER_SIZE)
		starts = (np.arange(self.echoes) + 1) * self.sampleDelay
		slices = np.array([starts, starts + self.nSamples])
		for i in range(self.echoes):
			delay[slices[0,i] : slices[1,i]] = chunk * (self.echoes - i)
		return signal + delay

	def set_params(self, **kwargs):
		self.sampleDelay = kwargs['sampleDelay']
		self.ratio = kwargs['ratio']
		self.nSamples = 256
		self.echoes = (BUFFER_SIZE // sampleDelay) - 1


class Chorus(object):

	def __init__(self, phase1=0.1, phase2=0.75):
		self.set_params(phase1=phase1, phase2=phase2)

	def get_effected_signal(self, signal):
		return 0.5 * signal * (1 + self.mod1 + self.mod2)

	def set_params(self, **kwargs):
		self.phase1 = kwargs['phase1']
		self.phase2 = kwargs['phase2']
		self.mod1 = np.sin(np.linspace(0 + phase1, 10 * np.pi + phase1,
			num=BUFFER_SIZE, endpoint=True))
		self.mod2 = np.sin(np.linspace(0 + phase2, 10 * np.pi + phase2,
			num=BUFFER_SIZE, endpoint=True))


class Tremolo(object):

	def __init__(self, freq=2.5, intensity=1.0):
		self.set_params(freq=freq, intensity=intensity)

	def get_effected_signal(self, signal):
		w = np.array(self.sin_wave)
		while len(w) < len(signal):
			w = np.append(w, self.sin_wave)
		self.sin_wave = np.roll(self.sin_wave, len(w)-len(signal))
		w = w[0:len(signal)]
		return signal*w

	def set_params(self, **kwargs):
		freq = kwargs['freq']
		intensity = kwargs['intensity']
		self.length = RATE/freq
		factor = float(freq) * np.pi * 2.0 / float(RATE)
		self.sin_wave = np.sin(np.arange(self.length) * factor)
		self.sin_wave = np.absolute(self.sin_wave)
		self.sin_wave = self.sin_wave*intensity
		self.sin_wave = self.sin_wave + (1-intensity)


class Harmonizer(object):

	def __init__(self, interval='fourth', wetness=.8):
		self.set_params(interval=interval, wetness=wetness)

	def get_effected_signal(self, signal):
		signal = signal + self.wetness*pitch_shift(signal, 
												   self.interval)
		return signal

	def set_params(self, **kwargs):
		self.interval = kwargs['interval']
		self.wetness = kwargs['wetness']


class Popcorn(object):

	def __init__(self, speed=500):
		self.set_params(speed=speed)

	def get_effected_signal(self, signal):
		shifted = np.roll(signal, int(100 * np.sin(time.clock() * self.speed)))
		return signal + shifted

	def set_params(self, **kwargs):
		self.speed = kwargs['speed']
		self.phase = time.clock() * self.speed

class Clipping(object):
    
    def __init__(self, threshold=.1):
        self.set_params(threshold=threshold)
    
    def get_effected_signal(self, signal):
        signal = stats.threshold(signal, -self.threshold, self.threshold)
        return (1.0/float(self.threshold))*signal

    def set_params(self, **kwargs):
        self.threshold = kwargs['threshold']


ALL_FX = [LowpassFilter, Reverb, Tremolo, Harmonizer,
		  SciFiDelay, Chorus, Popcorn, Clipping, Wah]
