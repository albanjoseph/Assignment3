import numpy as np
import matplotlib.pyplot as plt

#creates a second order filter:
class IIR2filter: #creating iir filter class
    def __init__(self, _b0, _b1, _b2, _a0, _a1, _a2): #constructer function
        self.b0 = _b0 #store a and b inside the class
        self.b1 = _b1
        self.b2 = _b2
        self.a0 = _a0
        self.a1 = _a1 
        self.a2 = _a2 
        self.buffer1 = 0 # initialising buffer variable
        self.buffer2 = 0

    def filter(self, x): #need to create two accumulators
        acc_input = self.a0*x - self.buffer1*self.a1 - self.buffer2*self.a2 #accumulator for IIR part
        acc_output = acc_input*self.b0 + self.buffer1*self.b1 + self.buffer2*self.b2 #FIR accumulator
        self.buffer2 = self.buffer1
        self.buffer1 = acc_input
        return acc_output

class IIRfilter: #chain of 2nd order filter
    def __init__(self, sos): #constructer function
        self.filt = [] #list of instances of IIR2Filter
        for x in range(len(sos)): #repeat for all rows in sos array
            self.filt.append(IIR2filter(sos[x][0], sos[x][1], sos[x][2], sos[x][3], sos[x][4], sos[x][5]))
            #creates IIR2Filter instance with sos array
            #and stores instance in list
    def filter(self, x): #chain of 2nd Order Filters
        inP = x #store incoming data point in inP
        for i in range(len(self.filt)): #repeat for all filters
            outP = self.filt[i].filter(inP) #output of filter[i]
            inP = outP #IIR filter output becomes input of next filter
        return outP

def response(sos): #plots frequency and impulse response from sos coeffs
    filt = IIRfilter(sos) #creates chain of 2nd order filters

    x=np.zeros(100,dtype=complex) #creating impulse response
    x[10]=1

    y=np.zeros(100,dtype=complex)
    for i in range(len(x)):
        y[i]= filt.filter(x[i]) #result of impulse response stored in y
        
    plt.figure(1)
    plt.plot(y) #plots impulse response
    plt.figure(2)
    plt.plot(np.linspace(0,1,len(y)), abs(np.fft.fft(y))) #plots transfer function
    plt.show()