"""
Recieve and send audio through running the main loop here.
Listen for changes in audio effects and their parameters.
"""

import pyaudio
import pygame as pg # take this out later
import numpy as np
import scipy.signal as sg
import time
import event_listener
from utils import *
from global_vars import *


def callback(in_data, frame_count, time_info, status):
    signal = decode(in_data)
    # TODO: Process FX chain here
    out_data = encode(signal)
    return (out_data, pyaudio.paContinue)


def main():
    p = pyaudio.PyAudio()
    
    pg.init() # take this out later

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(WIDTH),
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        if event_listener.event_listen_keyboard():
            break
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()

    p.terminate()
    pg.quit()

if __name__ == '__main__':
    main()