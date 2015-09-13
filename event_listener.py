"""
Listens for events. I.e. calls to change the current effects.
"""

import pygame as pg
from global_vars import *
from effects import *

KEYS = {pg.K_1 : LowpassFilter,
        pg.K_2 : Reverb,
        pg.K_3 : Tremolo,
        pg.K_4 : Harmonizer,
        pg.K_5 : SciFiDelay,
        pg.K_6 : Chorus,
        pg.K_7 : Popcorn,
        pg.K_8 : Distortion}

def event_listen_keyboard():
    for event in pg.event.get():
        if (event.type == pg.KEYDOWN) and (event.key == pg.K_ESCAPE):
            return True
        if (event.type == pg.KEYDOWN) and (event.key in KEYS):
            Effect = KEYS[event.key]
            if Effect in ACTIVE_FX:
                pass
                # remove effect here
            else:
                ACTIVE_FX.append(Effect())
            print len(ACTIVE_FX)