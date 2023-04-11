import numpy as np
import subprocess
import math
import cmath
import piGraph

pi=math.pi

data=list()
for i in range(1000):
	data.append(math.sin(pi*i/18)+3*math.sin(pi*i/3)+2*math.sin(pi*i/6.5)+4*math.sin(pi*i/2))
data=np.asarray(data)

def DFT():
	N=data.shape[0]				#number of elements
	piGraph.remote(N/2,7,100,1)		#graph setup
	n=np.arange(N)				#iterates N
	k=n.reshape((N,1))			#condenses n into blocks
	M=np.exp(-2j*np.pi*k*n/N)		#complex exponential of each block of k
	ret=np.dot(M,data)			#multiplication of data with respective value of M
	ret=np.absolute(ret)*2/N
	print data
	print ret
	for i in range(N/2):
        	if [i]!=0:
                	piGraph.remoteGraph(i,ret[i])

def FFT():
	bins=np.zeros([N],dtype=complex)
	eB=np.zeros([N/4],dtype=complex)
	oB=np.zeros([N/4],dtype=complex)
	eBB=np.zeros([N/4],dtype=complex)
        oBB=np.zeros([N/4],dtype=complex)
	for i in range(N/4):
		for m in range(N/4):
			eB[i] += data[4*m]*cmath.exp(-2j*pi*i*(4*m)/N)
			oB[i] += data[4*m+1]*cmath.exp(-2j*pi*i*(4*m+1)/N)
			eBB[i] += data[4*m+2]*cmath.exp(-2j*pi*i*(4*m+2)/N)
                        oBB[i] += data[4*m+3]*cmath.exp(-2j*pi*i*(4*m+3)/N)
	eB=abs(eB)
	oB=abs(oB)
	eBB=abs(eBB)
	oBB=abs(oBB)
	bins[::4]=eB
	bins[2::4]=oB
	bins[3::4]=eBB
        bins[4::4]=np.delete(oBB,-1)
	bins=abs(bins)*2/N
	for i in range(N/2):
       		piGraph.remoteGraph(i,bins[i])
