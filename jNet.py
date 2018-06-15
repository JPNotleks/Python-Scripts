import numpy as np
import operator
import random
import math
from graphics import *
from PIL import Image

######################SETUP#############################
def s(x):
	y=1/(1+math.e**(-x))
	if y==0.5: return 0
	else: return y
sigmoid=np.vectorize(s)
panel=GraphWin("jNet",1100,750,autoflush=False)

net=np.array([64,4,4,10]);maxNeurons=max(net);l=len(net)
dictPos=np.empty([l,maxNeurons],dtype=object)					#position array ([layers,neurons,contents (a,w,b)])
netA=np.zeros([l,maxNeurons]);netW=np.zeros([l,maxNeurons,maxNeurons]);netB=np.zeros([l,maxNeurons])

def dataSetup():
	rawData = np.genfromtxt('./optdigits.tra', delimiter=',')	#data import and slicing
	trainSet=rawData[:100,0:64]					#64 data points
	global labels;labels=rawData[:100,64]				#true values
	values=np.zeros([100,16])					#setup for image generation
	
	#for i in range(100):
	#	for k in range(16):
	#		values[i,k]=(np.sum(trainSet[i,2*k:2*k+2])+np.sum(trainSet[i,2*k+8:2*k+10]))/4			#graphic pixel reduction 64->16
	#		if i==1:
	#			print trainSet[i,2*k:2*k+2],trainSet[i,2*k+8:2*k+10]
	#for k in range(16):
	#		r=values[3,k]*15
	#		c=Circle(Point(30+(k%4)*20,100+math.floor(k/4)*20),10);c.setFill(color_rgb(r,r,r));c.draw(panel)	#graphing short set
	for k in range(64):
			r=trainSet[4,k]*15
	                c=Circle(Point(30+(k%8)*20,290+math.floor(k/8)*20),10);c.setFill(color_rgb(r,r,r));c.draw(panel)	#graphing long set
	global inputData;inputData=trainSet											#first entry of 64 points
dataSetup()


for i in range(l):							#point and matrix creation
	for k in range(net[i]):
		w=[];b=random.randint(-100,0)/500.0
		for j in range(maxNeurons):
			w.append(random.randint(-100,100)/100.0)
		p=Point(int(200+400/l+i*180),int(50+600*k/(net[i]-1)))
		dictPos[i,k]=p
		netA[i,k]=0;netW[i,k]=w;netB[i,k]=b
		c=Circle(p,6);c.draw(panel)

for i in range(1,l):							#weight graphing
	for k in range(net[i]):
		for r in range(net[i-1]):
			t=255/(1+math.e**(-3*netW[i,k,r]))
			line=Line(dictPos[i,k],dictPos[i-1,r]);line.setFill(color_rgb(t,t,t));line.draw(panel)

def frame(v):
	global netA;netA[0]=inputData[v]/16.0								#feed-forward using inputs
	for i in range(l-1):
		netA[i+1]=sigmoid(np.dot(netW[i+1],netA[i])+netB[i+1])
	#for i in range(l):
	#	for k in range(net[i]):
	#		c=Circle(dictPos[i,k],6);c.setFill(color_rgb(netA[i,k]*255,netA[i,k]*255,netA[i,k]*255));c.draw(panel)
	y=np.zeros([maxNeurons]);y[labels[v]]=1
	cost=np.sum((netA[-1]-y)**2);print cost
	#return [netA,netW,netB,cost];panel.update()
for i in range(100):
	frame(i)
