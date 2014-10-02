import sys
import pickle
from scipy import signal
import math, numpy
#from matplotlib import pyplot

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore,QtGui

# some constants
samp_rate = 128
sim_time = 5
nsamps = samp_rate*sim_time
cuttoff_freq = 40.0

#fig = pyplot.figure()
win = pg.GraphicsWindow()
win.setWindowTitle('Filtered FFT Plot')
p = win.addPlot()

# generate input signal
with open(sys.argv[1]) as eeg:
    net_eeg_data = pickle.load(eeg)

x = net_eeg_data[:nsamps,3]
#time_dom = fig.add_subplot(232)
#pyplot.plot(x)
#p.plot(x,pen='r')
#pyplot.title('Filter Input - Time Domain')
#pyplot.grid(True)

# input signal spectrum
xfreq = numpy.fft.fft(x)
fft_freqs = numpy.fft.fftfreq(nsamps, d=1./samp_rate)
#fig.add_subplot(233)
#pyplot.plot(fft_freqs[1:nsamps/2], numpy.abs(xfreq)[1:nsamps/2])
p.plot(fft_freqs[1:nsamps/2],100+numpy.abs(xfreq)[1:nsamps/2],pen='y')
#pyplot.title('Filter Input - Frequency Domain')
#pyplot.grid(True)

# design filter
norm_pass = cuttoff_freq/(samp_rate/2)
norm_stop = 3*norm_pass
(N, Wn) = signal.buttord(wp=norm_pass, ws=norm_stop, gpass=2, gstop=30, analog=0)
print N,Wn
(b, a) = signal.butter(N, Wn, btype='low', analog=0, output='ba')
#print("b="+str(b)+", a="+str(a))


# filtered output
#zi = signal.lfiltic(b, a, x[0:5], x[0:5])
#(y, zi) = signal.lfilter(b, a, x, zi=zi)
y = signal.lfilter(b, a, x)
#fig.add_subplot(235)
#pyplot.plot(y)
#p.plot(y,pen='y')
#pyplot.title('Filter output - Time Domain')
#pyplot.grid(True)

# output spectrum
yfreq = numpy.fft.fft(y)
#fig.add_subplot(236)
#pyplot.plot(fft_freqs[0:nsamps/2], numpy.abs(yfreq)[0:nsamps/2])
p.plot(fft_freqs[1:nsamps/2], numpy.abs(yfreq)[1:nsamps/2],pen='r')
#pyplot.title('Filter Output - Frequency Domain')
#pyplot.grid(True)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
