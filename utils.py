"""
Utility functions
"""

import numpy as np


def decode(data):
	return np.frombuffer(data, dtype=np.float32)


def encode(signal):
	return np.getbuffer(signal)