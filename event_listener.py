"""
Listens for events. I.e. calls to change the current effects.
"""

import pygame as pg
from effects import *

KEYS = {pg.K_1 : LowpassFilter}

def event_listen_keyboard():
    for event in pg.event.get():
            if (event.type == pg.KEYDOWN) and (event.key == pg.K_ESCAPE):
                return True
            if (event.type == pg.KEYDOWN) and (event.key in KEYS):
                effect = KEYS[event.key]
                if effect in ACTIVE_FX:
                    ACTIVE_FX.remove(effect)
                else:
                    ACTIVE_FX.append(effect)