"""
Utility functions
"""

import numpy as np


def decode(data):
	return np.fromstring(data, dtype='Float32')


def encode(signal):
	return signal.astype(np.float32).tostring()