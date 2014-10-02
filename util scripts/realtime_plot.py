from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import pickle
import numpy

sampling_frequency = 128
duration = 100

total_samples = duration*sampling_frequency

channels = ["F3", "FC5", "AF3", "F7", "T7", "P7", "O1", "O2", "P8",  "T8",  "F8", "AF4", "FC6", "F4"]
colors = ['b','g','r','m','y','c','k','b','g','r','m','y','c','k']

net_eeg_data = numpy.ndarray((total_samples,15),dtype=numpy.uint16)
with open('eeg_data.pickle') as eeg:
    net_eeg_data = pickle.load(eeg)

X_axis = numpy.linspace(0,100,total_samples)
eeg_data = net_eeg_data[:,1]


#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])
#mw = QtGui.QMainWindow()
#mw.resize(800,800)

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

p6 = win.addPlot(title="Updating plot")
curve = p6.plot(pen='r')
ydata = np.array_split(eeg_data,duration/2)
xdata = np.array_split(X_axis,duration/2)

ptr = 0
def update():
    global curve, data, ptr, p6
    curve.setData(xdata[0],ydata[ptr%50])
    curve.setPos(x,0)
    ptr += 1
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(1000)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

