
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import numpy as np
from scipy.io.wavfile import write





fig = plt.figure(figsize=[14,4])
N = 44100          # Number of samplepoints
Fs = 400
T = 1.0 / Fs      # N_samps*T (#samples x sample period) is the sample spacing.
N_fft = 80        # Number of bins (chooses granularity)
x = np.linspace(0, N*T, N)     # the interval

def funGen( x, baseFreq = 50, iterations = 1000):
    
   baseFreq = 50
   y= np.sin(baseFreq * 2.0*np.pi*x)
   
   for i in range(iterations):
       nHarm=i+1
       y = y+ 1/nHarm*np.sin(2*nHarm*baseFreq * 2.0*np.pi*x)
       
   
   
   return y
y = funGen(x, 50, 1)   # the signal

t= np.linspace(0,1,44100)
Freq= 0.25*440; #Freq in HZ
data = np.sin(t*2*np.pi*Freq) # 44100 random samples between -1 and 1

def createSin(Freq,t=np.linspace(0,1/Freq)):
    sin = np.sin(t*2*np.pi*Freq)
    return sin

def addOp( t,data, Freq = 440, iterations = 3, nthHarm=2, harmDecay=1): # (t-wertem, Amplitutem, Freq in HZ,numberOF FM Operatoror
   for i in range(iterations):
       nHarm=i+1
       data = data+ (1/nHarm)*np.sin(nthHarm*nHarm*Freq * 2.0*np.pi*t)
   
   return data

def FmOp( t,data, Freq = 440, iterations = 1, nthHarm=1): # (t-wertem, Amplitutem, Freq in HZ,numberOF FM Operatoror
   for i in range(iterations):
       nHarm=i+1
       data = data* 1/nHarm*np.sin(nthHarm*nHarm*Freq * 2.0*np.pi*t)
   
   return data


def WavExport(data,fileName = 'waveform.wav'):
    scaled = np.int16(data/np.max(np.abs(data)) * 32767)
#scaled = np.int16(y/np.max(np.abs(y)) * 32767)
    dataF= str(fileName)
    write(dataF, 44100, scaled)  
    return       
    WavExport(data,'deineMutta.wav') 

for i in range(100):
    print(i)
    data= addOp(t,data,Freq, i+1, np.sin(i)) 
   
    
    WavExport(data,'addOp'+str(i)+'.wav')
    data= FmOp(t,data,Freq, i+1, 1) 
    WavExport(data,'FmOp'+str(i)+'.wav')
    data= np.sin(t*2*np.pi*Freq)
    data= addOp(t,data,Freq, i+1, 5 ) 
    WavExport(data,'sinSqrtHarm'+str(i)+'.wav')
#scaled = np.int16(data/np.max(np.abs(data)) * 32767)
#scaled = np.int16(y/np.max(np.abs(y)) * 32767)
#write('test.wav', 44100, scaled)
          
y= addOp(t,data,Freq, 2, 2) 
 
   


t = np.linspace(0,1/Freq,100)
sin = np.sin(t*2*np.pi*Freq)
data= addOp(t,sin,Freq, 100, sin ) 
WavExport(data,'SinTHHarm.wav')

def oneCycle(data,Freq):
    t = np.linspace(0,1/Freq,np.size(data))
    sin = np.sin(t*2*np.pi*Freq)
    plt.figure(2)
    plt.plot( t,data)
    plt.plot(t, sin)
    plt.ylabel('tau')
    plt.show()
    return 
# removing the mean of the signal

oneCycle(data, Freq)


plt.plot(np.linspace(0,10),createSin(440))
data = FmOp(np.linspace(0,10),data, Freq = 440, iterations = 1, nthHarm=1)
plt.plot(np.linspace(0,10),createSin(440))