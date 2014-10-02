# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""
#import initExample ## Add path to library (just for examples; you do not need this)
import sys
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pickle
from  scipy.fftpack import fft,fftfreq

sampling_frequency = 128
duration = 100

total_samples = duration*sampling_frequency

channels = ["F3", "FC5", "AF3", "F7", "T7", "P7", "O1", "O2", "P8",  "T8",  "F8", "AF4", "FC6", "F4"]
colors = ['b','g','r','m','y','c','k','b','g','r','m','y','c','k']

net_eeg_data = np.ndarray((total_samples,15),dtype=np.uint16)
with open(sys.argv[1]) as eeg:
    net_eeg_data = pickle.load(eeg)

win = pg.GraphicsWindow()
win.setWindowTitle('EEG Live Monitor')


# 1) Simplest approach -- update data in the array such that plot appears to scroll
#    In these examples, the array size is fixed.
p1 = win.addPlot()

#eeg_data = []
#curve = []
#for i in range(14):
#    eeg_data.append(net_eeg_data[:600,i+1])
#    curve.append(p1.plot(eeg_data[i],pen=colors[i]))


N = 128*5
eeg_data = net_eeg_data[:N,1]
Fs = 128

E = fft(eeg_data)
x_f = np.linspace(0,Fs,N)
freq = fftfreq(N,1/128.0)
#print np.around(np.floor(np.real((E))))
p1.plot(freq[0:N/2],np.abs(E)[0:N/2],pen='r')

"""index = 600
def update1():
    global index
    data = net_eeg_data[index]

    for i in range(14):
        eeg_data[i][:-1] = eeg_data[i][1:]

    for (i,d) in enumerate(data[1:]):
        eeg_data[i][-1] = d

    for i in range(14):
        curve[i].setData(eeg_data[i])

    index += 1

timer = pg.QtCore.QTimer()
timer.timeout.connect(update1)
timer.start(50)
"""


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
