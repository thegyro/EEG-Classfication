import sys
import pickle

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore,QtGui

from scipy.signal import butter, lfilter,freqz,filtfilt
import numpy as np
from scipy.fftpack import fft,fftfreq

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandpass')
    return b, a
  
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

with open(sys.argv[1]) as eeg:
    net_eeg_data = pickle.load(eeg)

N = 128*5
eeg_data1 = net_eeg_data[:N,1]
eeg_data2 = net_eeg_data[:N,3]

fs = 128
lowcut = 0.5
highcut = 40

filtered1 = butter_bandpass_filter(eeg_data1,lowcut,highcut,fs,6)
filtered2 = butter_bandpass_filter(eeg_data2,lowcut,highcut,fs,6)

win = pg.GraphicsWindow()
win.setWindowTitle('Filtered FFT Plot')
p = win.addPlot()

for order in [3,6,9]:
    b,a = butter_bandpass(lowcut,highcut,fs,order)
    w,h = freqz(b,a,worN = 200)
   # p.plot((fs*0.5/np.pi)*w,abs(h))

E1 = fft(filtered1)
E2 = fft(filtered2)
x_f = np.linspace(0,fs,N)
freq = fftfreq(N,1/128.0)
pre_E1 = fft(eeg_data1)
pre_E2 = fft(eeg_data2)

#p.plot(freq[1:N/2],np.abs(filtered[1:N/2]),pen='r')
#p.plot(freq[:N/2],np.abs(E1)[:N/2],pen='r')
#p.plot(freq[1:N/2],np.abs(pre_E1)[1:N/2],pen='b')
#p.plot(eeg_data1 - eeg_data2,pen='r')
#p.plot(filtered1 - filtered2,pen='y')
p.plot(filtered1,pen='y')
p.plot(eeg_data1,pen='r')

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
