#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 00:50:01 2017

@author: stefanreuteler
"""

import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
import numpy as np

from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

root = Tk.Tk()
root.wm_title("Embedding in TK")


f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)

def createSin(Freq):
    t=np.linspace(0,1/Freq)
    sin = np.sin(t*2*np.pi*Freq)
    return [t, sin]

def fmOp(data, Freq = 440, iterations = 3, nthHarm=2): # (t-wertem, Amplitutem, Freq in HZ,numberOF FM Operatoror
    t= data[0]
    A_data = data[1]
    for i in range(iterations):
       nHarm=i+1
       A_data = A_data* (1/nHarm)*np.sin(nthHarm*nHarm*Freq * 2.0*np.pi*t)
       A_data=A_data/np.max(A_data)   
    return [t, A_data]

t,sin = createSin(440)
t, s = fmOp([t,sin], 440, 2 , 2)


a.plot(t, s)
a.plot(t,sin)
Freq=440;

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


def on_key_event(event):
    print('you pressed %s' % event.key)
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def _frqChange(Freq,t,sin):
    Freq=Freq+10
    fmOp([t,sin], Freq, 2 , 2)
    a.plot(t,sin)

button = Tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)

button2 = Tk.Button(master=root, text='Quit', command=_frqChange(Freq,t,sin))
button2.pack(side=Tk.BOTTOM)

Tk.mainloop()
# If you put roo