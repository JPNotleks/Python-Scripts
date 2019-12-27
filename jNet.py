import numpy as np
import operator
import random
import math
from graphics import *
from PIL import Image
import piGraph
import json, codecs

######################SETUP############################

def s(x,deriv):
	y=np.piecewise(x,[x==0,x!=0],[0,1/(1+math.e**(-x))])
	if deriv==0: return y
	else: return y*(1-y)
sigmoid=np.vectorize(s)
panel=GraphWin("jNet",1100,750,autoflush=False)

eta=0.05;maxNeurons=0;l=0;net=0;netA=0;netB=0;netW=0;l=0;maxNeurons=0;dictPos=0;gradientW=0;gradientA=0;gradientB=0;gradientD=0
regressionData=np.zeros([30])
historyW=0;historyB=0;historyIndices=0
#neuronWSave=open("neuronWeightInitialisation","w+")
#neuronBSave=open("neuronBiasInitialisation","w+")
#netSave=open("netSave","w+")

myData=np.zeros([30])
for i in range(30):
	regressionData[i]=3*math.sin(2*i)+1.5	# 3,2,1.5

def neuralNet(yeet):
	global net;global netA;global netB;global netW;global l;global maxNeurons;global dictPos;global gradientW
	global gradientA;global gradientB;global gradientD
	piGraph.init(0,100,0,2,25,0.2,1)
	if yeet==0:
		net=np.array(json.loads(codecs.open("netSave.json", 'r', encoding='utf-8').read()))
	else:
		net=np.array(yeet)
	maxNeurons=max(net);l=len(net)
	dictPos=np.empty([l,maxNeurons],dtype=object)                                   #position array ([layers,neurons,contents (a,w,b)])
	netA=np.zeros([l,maxNeurons]);netW=np.zeros([l,maxNeurons,maxNeurons]);netB=np.zeros([l,maxNeurons])
	gradientW=np.zeros([l,maxNeurons,maxNeurons]);gradientA=np.zeros([l,maxNeurons]);gradientB=np.zeros([l,maxNeurons]);gradientD=np.zeros([l,maxNeurons])
	if yeet==0:
		netW=np.array(json.loads(codecs.open("neuronWSave.json", 'r', encoding='utf-8').read()))
		netB=np.array(json.loads(codecs.open("neuronBSave.json", 'r', encoding='utf-8').read()))
	else:
		netW=np.random.randint(-100,0,size=netW.shape)/500.0;netW[0,:]=0
		for i in range(l):
			netW[i,:,net[i-1]:]=0
			netW[i,net[i]:]=0
	print netW
	for i in range(l):
		for k in range(net[i]):
			p=Point(int(200+400/l+i*180),int(50+600*k/(net[i]-1)));dictPos[i,k]=p
	graph()

def clear():panel.delete("all")

def dataSetup():
	rawData = np.genfromtxt('./optdigits.tra', delimiter=',')	#data import and slicing
	trainSet=rawData[:,0:64]					#64 data points
	global labels;labels=rawData[:,64]				#true values
	values=np.zeros([1000,16])					#setup for image generation
	
	for i in range(1000):
		for k in range(16):
			values[i,k]=(np.sum(trainSet[i,2*k:2*k+2])+np.sum(trainSet[i,2*k+8:2*k+10]))/4			#graphic pixel reduction 64->16
	for k in range(64):
			r=trainSet[1,k]*15
	                c=Circle(Point(30+(k%8)*20,290+math.floor(k/8)*20),10);c.setFill(color_rgb(r,r,r));c.draw(panel)	#graphing long set
	global inputData;inputData=trainSet											#first entry of 64 points

dataSetup()
#neuralNet([64,10])

def graph():
	clear()
	for i in range(1,l):
		for k in range(net[i]):
			for r in range(net[i-1]):
				t=255/(1+math.e**(-3*netW[i,k,r]))
				line=Line(dictPos[i,k],dictPos[i-1,r]);line.setFill(color_rgb(t,t,t));line.draw(panel)
	for i in range(l):
                        for k in range(net[i]):
                                c=Circle(dictPos[i,k],6);c.setFill(color_rgb(netA[i,k]*255,netA[i,k]*255,netA[i,k]*255));c.draw(panel)
	for k in range(64):
                        r=inputData[1,k]*15
                        c=Circle(Point(30+(k%8)*20,290+math.floor(k/8)*20),10);c.setFill(color_rgb(r,r,r));c.draw(panel)
graph()

def frame(v,graphics):
	global netA;netA[0]=inputData[v]/16.0								#feed-forward using inputs
	for i in range(l-1):
		netA[i+1]=sigmoid(np.dot(netW[i+1],netA[i])+netB[i+1],0)
	if graphics==1:
		graph()
	y=np.zeros([maxNeurons]);y[int(labels[v])]=1
	cost=np.sum((netA[-1][:net[-1]]-y[:net[-1]])**2)/2
	out=np.array([y,netA,netW,netB,cost])
	return out

def backprop(input):
	global netA,netW,gradientA,gradientB,gradientW,gradientD
	g=input
	gradientD[-1]=(netA[-1]-g[0])*sigmoid(netA[-1],1)		#dC/dA for deltas
	
	for k in range(2,l):
		gradientD[-k]=sigmoid(netA[1-k],1)*(np.dot(netW[-k],np.reshape(gradientD[1-k],maxNeurons)))    #sigma' (hadamard) (w*gradient.T)
	gradientB=gradientD
	for i in range(1,l-1):
		for k in range(net[i]):
			gradientW[i,k]=netA[i-1]*gradientD[i,k]
	return [gradientW,gradientB,g[4]]

def train(epoch,maxIter,batch,rate):
	global netW,netB,historyIndices,historyW,historyB;best=0;b=float(batch)
	print epoch*maxIter
	historyW=np.expand_dims(np.zeros(netW.shape),0)
	historyB=np.expand_dims(np.zeros(netB.shape),0)
	historyIndices=np.full((epoch*maxIter,2),100.0)
	for r in range(epoch):
		#if best!=0:
		#	netW=historyW[best]
		#	netB=historyB[best]
		#	print historyIndices[best]
		for u in range(int(maxIter/b)):
			g=u+r*int(maxIter/b)
			tA=np.zeros([l,maxNeurons]);tW=np.zeros([l,maxNeurons,maxNeurons]);tB=np.zeros([l,maxNeurons]);tC=0
			for i in range(batch):
				p=backprop(frame(r*int(maxIter/b)+u*batch+i,1))
				tW+=p[0]
				tB+=p[1]
				tC+=p[2]
			tW=tW/b;tB=tB/b;tC=tC/b
			print "cost at iteration"+" "+str(g)+" "+str(round(tC,3))
			netW=netW-rate*tW;netB=netB-rate*tB
		#	historyIndices[g]=[g,tC]
		#	historyW[g]=netW;historyB[g]=netB
			piGraph.pointPlot(g,tC,2,"black")
		#best=np.argsort(historyIndices[:,1])[0]
		#print best

def restore(n):
	netW=historyW[n]
	netB=historyB[n]

def regression():
	setGraph([3,30]);graph();global netA
	a=1.0;b=1.0;c=1.0
	for u in range(30):
		netA[0,0]=1.0
		netA[0,1]=1.0
		netA[0,2]=1.0
        	for i in range(l-1):
        	        netA[i+1]=sigmoid(np.dot(netW[i+1],netA[i])+netB[i+1])
		for i in range(30):
			myData[i]=a*math.sin(b*i)+c
		y=regressionData;cost=np.sum((regressionData-myData)**2)
		b=backprop(np.array([y,netA,netW,netB,cost]),1)
		totalGradient0=np.sum(b[0][-1,:,0])
		totalGradient1=np.sum(b[0][-1,:,1])
		totalGradient2=np.sum(b[0][-1,:,2])
		netW[-1,:,0]+=-eta*totalGradient0;a+=-eta*totalGradient0
		netW[-1,:,1]+=-eta*totalGradient1;b+=-eta*totalGradient1
		netW[-1,:,2]+=-eta*totalGradient2;c+=-eta*totalGradient2

def classify(start,i):
	counter=0.0
	for u in range(i):
		g=frame(start+u,0)
		if np.argmax(g[1][-1])==labels[start+u]:
			print "correct, "+str(np.argmax(g[1][-1]))
			counter+=1
		else:
			print "wrong, got "+str(np.argmax(g[1][-1]))+" instead of "+str(int(labels[start+u])	)
	print "total "+str(100.0*counter/i)

def save():
	json.dump(netW.tolist(),codecs.open("neuronWSave.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
	json.dump(netB.tolist(),codecs.open("neuronBSave.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
	json.dump(net.tolist(),codecs.open("netSave.json", 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
