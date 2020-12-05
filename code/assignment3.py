from pyfirmata2 import Arduino
import realtimescope as rts
import scipy.signal as signal
import IIR_filter as IIR
import sys
from pyqtgraph.Qt import QtGui #pyqtgraph plots different channels in seperate windows
from timer import Timer

t = Timer() #timer object

app = QtGui.QApplication(sys.argv) #create a global QT application object
running = True #signals to all threads in endless loops that we'd like to run these

qtPanningPlot1 = rts.QtPanningPlot("Arduino 1st channel") #Two instances of plot windows
qtPanningPlot2 = rts.QtPanningPlot("Arduino 2nd channel")

samplingRate = 100 #sampling rate: 100Hz

f1 = 1
sos = signal.butter(5,2*f1/samplingRate, output = 'sos')
#sos = signal.butter(2,[2*f1/samplingRate, 2*f2/samplingRate], 'stop', output = 'sos') #normalised to nyquist
#IIR.response(sos)
filt = IIR.IIRfilter(sos) #filter object instantiated

def resetTimer(x):
    x.stop() #stops timer
    x.sampleCount = 0 #resets internal variable
    x.start() #starts timer again

# called for every new sample at channel 0 which has arrived from the Arduino
# "data" contains the new sample
def callBack(data):
    #channel 0 data sent to the plotwindow
    qtPanningPlot1.addData(data)
    ch1 = board.analog[1].read()
    # 1st sample of 2nd channel might arrive later so need to check
    if ch1:
        print(t.frequency(), "Hz")
        t.reset()
        # filtering channel 1 samples here:
        ch1 = filt.filter(data) 
        qtPanningPlot2.addData(ch1)


PORT = Arduino.AUTODETECT #Get the Ardunio board.
board = Arduino(PORT)

board.samplingOn(1000 / samplingRate) # Set the sampling rate in the Arduino
# Register the callback which adds the data to the animated plot
t.start() #starts timer
board.analog[0].register_callback(callBack) #The function "callback" is called when data has arrived

board.analog[0].enable_reporting() #Enable the callback
board.analog[1].enable_reporting()

app.exec_() #showing all the windows
board.exit() #needs to be called to close the serial port
print("finished")