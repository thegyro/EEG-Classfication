import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pickle

with open('live_eeg.pickle') as eeg:
    eeg_data = pickle.load(eeg)

win = pg.GraphicsWindow()
win.setWindowTitle('EEG Live Monitor')


# 1) Simplest approach -- update data in the array such that plot appears to scroll
#    In these examples, the array size is fixed.
p1 = win.addPlot()
#p2 = win.addPlot()

X_axis = np.linspace(0,1000,128000)
batch_x = X_axis[:100]
curve1 = p1.plot(batch_x,batch_y,pen='r')
#p1.setYRange(1800,2600)
#curve2 = p2.plot(data1,pen='y')

ptr1 = 0
index = 101
def update1():
    global data1, curve1, ptr1,index
    batch_x[:-1] = batch_x[1:]  # shift data in the array one sample left
                            # (see also: np.roll)
    batch_x[-1] = X_axis[index]

    with open('new_data.pickle') as new:
        to_be_added = pickle.load(new)
    
    eeg_data[:-1] = eeg_data[1:]
    eeg_data[-1] = to_be_added

    curve1.setData(batch_x,batch_y)
    index += 1

    if(index == 12800):
        index = 0
#    ptr1 += 1
#    curve2.setData(data1)
#    curve2.setPos(ptr1, 0)
    

timer = pg.QtCore.QTimer()
timer.timeout.connect(update1)
timer.start(50)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
