import pyaudio
import struct
import numpy as np
import piGraph

piGraph.init(0,100,0,100,10,10,1)

audioChunk=4*4096
audioFormat=pyaudio.paInt16
audioRate=44100

p=pyaudio.PyAudio()

stream=p.open(
	format=audioFormat,
	channels=1,
	rate=audioRate,
	input=True,
	output=True,
	frames_per_buffer=audioChunk
)

data=stream.read(audioChunk)
data_int=np.fromstring(data,'int')
print data_int
p.terminate()
