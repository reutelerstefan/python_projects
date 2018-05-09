import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy import signal



def createSin(Freq):
    t=np.linspace(0,1/Freq)
    sin = np.sin(t*2*np.pi*Freq)
    return [t, sin]
def createSaw(start,stop, Freq):
    t = np.linspace(start, stop, 500)
    plt.figure(3)
    saw=signal.sawtooth(2 * np.pi * 5 * t)
    plt.plot(t, signal.sawtooth(2 * np.pi * 5 * t))
    return [t, saw]

def plotCycle(data):
    t_data= data[0]
    A_data = data[1]
    plt.figure(1)
    plt.plot( t_data,A_data)
    plt.ylabel('tau')
    plt.show()
    return 

def addOp(data, Freq = 440, iterations = 3, nthHarm=2): # (t-wertem, Amplitutem, Freq in HZ,numberOF FM Operatoror
    t= data[0]
    A_data = data[1]
    for i in range(iterations):
       nHarm=i+1
       A_data = A_data+ (1/nHarm)*np.sin(nthHarm*nHarm*Freq * 2.0*np.pi*t)   
       A_data=A_data/np.max(A_data)
    return [t, A_data]

def fmOp(data, Freq = 440, iterations = 3, nthHarm=2): # (t-wertem, Amplitutem, Freq in HZ,numberOF FM Operatoror
    t= data[0]
    A_data = data[1]
    for i in range(iterations):
       nHarm=i+1
       A_data = A_data* (1/nHarm)*np.sin(nthHarm*nHarm*Freq * 2.0*np.pi*t)
       A_data=A_data/np.max(A_data)   
    return [t, A_data]

def WavExport(data,fileName = 'waveform.wav'):
    data = data[1]
    scaled = np.int16(data/np.max(np.abs(data)) * 32767)
#scaled = np.int16(y/np.max(np.abs(y)) * 32767)
    dataF= str(fileName)
    write(dataF, 44100, scaled)  
    return       





Freq= 440*0.25;


dataSin = createSin(Freq)
plotCycle(dataSin)
dataOp= addOp(dataSin, Freq, 1, 2)
plotCycle(dataOp)
dataOp= fmOp(dataSin, Freq, 2, 3)
createSaw(0,1, Freq)
plotCycle(dataOp)

WavExport(dataOp, 'testliq.wav')
t, saw=createSaw(0,1, Freq)


fourier = np.fft.fft(saw)
n = saw.size

timestep = 0.1
freq = np.fft.fftfreq(n, d=timestep)
ind = np.arange(1,n/2+1)
ind = ind.astype(int)
freq[ind]

plt.figure(4)

plt.plot(t,fourier,'x')