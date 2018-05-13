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

net=np.array([6,4,4,4]);maxNeurons=max(net);l=len(net)
dictPos=np.empty([l,maxNeurons],dtype=object)					#position array ([layers,neurons,contents (a,w,b)])
netA=np.zeros([l,maxNeurons]);netW=np.zeros([l,maxNeurons,maxNeurons]);netB=np.zeros([l,maxNeurons])
cost=0										#cost function
inputData=1

def dataSetup():
	rawData = np.genfromtxt('./optdigits.tra', delimiter=',')	#data import and slicing
	trainSet=rawData[:100,0:64]					#64 data points
	labels=rawData[:100,64]						#true values
	values=np.zeros([100,16])					#setup for image generation
	
	for i in range(100):
		for k in range(16):
			values[i,k]=(np.sum(trainSet[i,2*k:2*k+2])+np.sum(trainSet[i,2*k+8:2*k+10]))/4		#graphic pixel reduction 64->16
	
	for k in range(16):
			r=values[2,k]*15
			c=Circle(Point(30+(k%4)*20,100+math.floor(k/4)*20),10);c.setFill(color_rgb(r,r,r));c.draw(panel)	#graphing short set
	for k in range(64):
			r=trainSet[2,k]*15
	                c=Circle(Point(30+(k%8)*20,300+math.floor(k/8)*20),10);c.setFill(color_rgb(r,r,r));c.draw(panel)	#graphing long set
	inputData=trainSet[0,:];print trainSet[0,:]			#first entry of 64 points

dataSetup()

for i in range(l):							#point and matrix creation
	for k in range(net[i]):
		w=[];b=random.randint(-100,0)/200.0
		for j in range(maxNeurons):
			w.append(1)#random.randint(-100,100)/100.0)
		p=Point(int(200+400/l+i*180),int(600-500*k/(net[i]-1)))
		dictPos[i,k]=p
		netA[i,k]=0;netW[i,k]=w;netB[i,k]=b
		c=Circle(p,6);c.draw(panel)

for i in range(1,l):							#weight graphing
	for k in range(net[i]):
		for r in range(net[i-1]):
			t=255/(1+math.e**(-3*netW[i,k,r]))
			line=Line(dictPos[i,k],dictPos[i-1,r]);line.setFill(color_rgb(t,t,t));line.draw(panel)

def frame():								#feed-forward using inputs
	for i in range(l-1):
		netA[i+1]=sigmoid(np.dot(netW[i+1],netA[i])+netB[i+1])
		for k in range(net[i+1]):
			c=Circle(dictPos[i+1,k],6);c.setFill(color_rgb(netA[i+1,k]*255,netA[i+1,k]*255,netA[i+1,k]*255));c.draw(panel)
	return netA[-1];panel.update()
print frame()

#for i in range (1,l):
#        for k in range(net[i]):
#                print dictPos[i][k][0]
#                c=Circle(dictPos[i][k][0],6);c.setFill(color_rgb(dictPos[i][k][1]*255,dictPos[i][k][1]*255,dictPos[i][k][1]*255));c.draw(panel)
