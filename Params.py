from tkinter import *
from math import ceil

COLOR_BG    = '#D4EFDF'
COLOR_INPUT = '#145A32'
COLOR_FONT  = '#145A32'
COLOR_FONT_INPUT = '#D4EFDF'
FONT = ('calibri','13','bold')
FONT_OP = ('calibri','12')

PADX = 5
PADY = 5

W = 550
H = 600


def converter_pixel_chr(w, pad = True):
    '''width dos componentes possui medida de Caracter'''
    if pad:
        return ceil((w*0.125) - (PADX*0.125))
    return ceil(w*0.125)
