"""
Listens for events. I.e. calls to change the current effects.
"""

import urllib.request
from effects import *


def get_web_info(address):
    info = urllib.request.urlopen(address).read()
    
    if info[5] == "True":
        if "Lowpass Filter" in ACTIVE_FX.keys():
            ACTIVE_FX["Lowpass Filter"].set_params(cut_off_freq=info[6])
        else:
            ACTIVE_FX["Lowpass Filter"] = LowpassFilter()
    else:
        if "Lowpass Filter" in ACTIVE_FX.keys():
            del ACTIVE_FX["Lowpass Filter"]

    if info[8] == "True":
        if "Highpass Filter" in ACTIVE_FX.keys():
            ACTIVE_FX["Highpass Filter"].set_params(cut_off_freq=info[6])
        else:
            ACTIVE_FX["Highpass Filter"] = HighPassFilter()
    else:
        if "Highpass Filter" in ACTIVE_FX.keys():
            del ACTIVE_FX["Highpass Filter"]

    if info[11] == "True":
        if "Delay" in ACTIVE_FX.keys():
            pass
        else:
            ACTIVE_FX["Delay"] = Delay()
    else:
        if "Delay" in ACTIVE_FX.keys():
            del ACTIVE_FX["Delay"]

    if info[14] == "True":
        if "Tremolo" in ACTIVE_FX.keys():
            pass
        else:
            ACTIVE_FX["Tremolo"] = Tremolo()
    else:
        if "Tremolo" in ACTIVE_FX.keys():
            del ACTIVE_FX["Tremolo"]

    if info[17] == "True":
        if "Chorus" in ACTIVE_FX.keys():
            pass
        else:
            ACTIVE_FX["Chorus"] = Chorus()
    else:
        if "Chorus" in ACTIVE_FX.keys():
            del ACTIVE_FX["Chorus"]

    if info[20] == "True":
        if "Harmonizer" in ACTIVE_FX.keys():
            pass
        else:
            ACTIVE_FX["Harmonizer"] = Harmonizer()
    else:
        if "Harmonizer" in ACTIVE_FX.keys():
            del ACTIVE_FX["Harmonizer"]

    if info[23] == "True":
        if "Distortion" in ACTIVE_FX.keys():
            ACTIVE_FX["Distortion"].set_params(threshold=info[24Wah])
        else:
            ACTIVE_FX["Distortion"] = Distortion()
    else:
        if "Distortion" in ACTIVE_FX.keys():
            del ACTIVE_FX["Distortion"]

    if info[26] == "True":
        if "Wah" in ACTIVE_FX.keys():
            ACTIVE_FX["Wah"].set_params(cut_off_freq=info[27])
        else:
            ACTIVE_FX["Wah"] = Wah()
    else:
        if "Wah" in ACTIVE_FX.keys():
            del ACTIVE_FX["Wah"]

    if info[29] == "True":
        if "Popcorn" in ACTIVE_FX.keys():
            pass
        else:
            ACTIVE_FX["Popcorn"] = Popcorn()
    else:
        if "Popcorn" in ACTIVE_FX.keys():
            del ACTIVE_FX["Popcorn"]

    if info[32] == "True":
        if "Sci-Fi Delay" in ACTIVE_FX.keys():
            ACTIVE_FX["Sci-Fi Delay"].set_params(cut_off_freq=info[6])
        else:
            ACTIVE_FX["Sci-Fi Delay"] = SciFiDelay()
    else:
        if "Sci-Fi Delay" in ACTIVE_FX.keys():
            del ACTIVE_FX["Sci-Fi Delay"]

    if info[35] == "True":
        value = float(info[36])
        if "Harmonizer" in ACTIVE_FX.keys():
            pass
        else:
            ACTIVE_FX["Harmonizer"] = Harmonizer()
        if value < -0.3:
            ACTIVE_FX["Harmonizer"].set_params(interval='tritone', wetness=0.8)
        elif (value >= -0.3) and (value < 0.3):
            ACTIVE_FX["Harmonizer"].set_params(interval='fourth', wetness=0.8)
        else:
            ACTIVE_FX["Harmonizer"].set_params(interval='fifth', wetness=0.8)
