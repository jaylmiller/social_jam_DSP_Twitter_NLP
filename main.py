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
    #if len(ACTIVE_FX) == 0:
    #    return (in_data, pyaudio.paContinue)

    signal = decode(in_data)
    
    print pitch_detect_fft_bins(signal), pitch_detect_zero_crossing(signal)

    for effect in ACTIVE_FX:
        signal = effect.get_effected_signal(signal)
    return (encode(signal), pyaudio.paContinue)


def main():
    p = pyaudio.PyAudio()
    
    pg.init() # take this out later

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paFloat32,
                    channels=CHANNELS,
                    rate=RATE,
                    frames_per_buffer = BUFFER_SIZE,
                    input=True,
                    output=True,
                    stream_callback=callback)

    stream.start_stream()

    try:
        while stream.is_active():
            if event_listener.event_listen_keyboard():
                break
            time.sleep(5)
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()

    p.terminate()
    pg.quit()

if __name__ == '__main__':
    main()