#import pyqtgraph as pg
#from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pickle
import pyeeg
import sys
import pylab
from filter_test import butter_bandpass_filter


with open(sys.argv[1]) as eeg:
    net_eeg_data = pickle.load(eeg)


N = 500
Fs = 128

eeg_data = butter_bandpass_filter(net_eeg_data[:N,1].astype(np.int64) - net_eeg_data[:N,3].astype(np.int64),4,40,128,4)
freq = [0.5,4,7,12,30,40,50]
#freq = np.linspace(4,40,N)
power,ratio = pyeeg.bin_power(eeg_data,freq,Fs)

pylab.plot(freq[:-1],power,color='r')
pylab.show()