"""
Utility functions
"""

import numpy as np
import scipy.signal as signal


def decode(data):
	return np.frombuffer(data, dtype=np.float32)


def encode(signal):
	return signal.astype(np.float32).tostring()