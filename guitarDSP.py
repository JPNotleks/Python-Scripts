import matplotlib.pyplot as plt
import numpy as np
from pyAudioAnalysis import audioFeatureExtraction
from pyAudioAnalysis import audioBasicIO
import wave

analysis, plots = plt.subplots(nrows=2, ncols=2)
fftPlot=plots[0,0]
fftPlot.set(xlim=[20,20000],ylim=[0.0000001,1000000],xscale="log",yscale="log",title="fft plot",xlabel="Hz",ylabel="dB")
fftPlot.plot([100,2000,3000,4000],[2,0.01,18,6])

from matplotlib.ticker import ScalarFormatter
fftPlot.xaxis.set_major_formatter(ScalarFormatter())

print(audioBasicIO.readAudioFile("FirstSoundTest.wav"))

plt.show(analysis)
