import numpy as np
import operator
import random
import math
from graphics import *
from PIL import Image

######################SETUP#############################
def s(x):
	if x>10 or x<-10:y=1
	else:y=1/(1+math.e**(-x))
	if y==0.5: return 0
	else: return y
sigmoid=np.vectorize(s)
panel=GraphWin("jNet",1100,750,autoflush=False)

net=np.array([64,10,10]);maxNeurons=max(net);l=len(net);eta=0.5
dictPos=np.empty([l,maxNeurons],dtype=object)					#position array ([layers,neurons,contents (a,w,b)])
netA=np.zeros([l,maxNeurons]);netW=np.zeros([l,maxNeurons,maxNeurons]);netB=np.zeros([l,maxNeurons])
gradientW=np.zeros([l,maxNeurons,maxNeurons]);gradientA=np.zeros([l,maxNeurons]);gradientB=np.zeros([l,maxNeurons])
costIndex=np.array([]);WList=np.array([]);BList=np.array([])

def clear():
        panel.delete("all")

def dataSetup():
	rawData = np.genfromtxt('./optdigits.tra', delimiter=',')	#data import and slicing
	trainSet=rawData[:,0:64]					#64 data points
	global labels;labels=rawData[:,64]				#true values
	values=np.zeros([1000,16])					#setup for image generation
	
	for i in range(1000):
		for k in range(16):
			values[i,k]=(np.sum(trainSet[i,2*k:2*k+2])+np.sum(trainSet[i,2*k+8:2*k+10]))/4			#graphic pixel reduction 64->16
	#for k in range(16):
	#		r=values[1,k]*15
	#		c=Circle(Point(30+(k%4)*20,100+math.floor(k/4)*20),10);c.setFill(color_rgb(r,r,r));c.draw(panel)	#graphing short set
	for k in range(64):
			r=trainSet[1,k]*15
	                c=Circle(Point(30+(k%8)*20,290+math.floor(k/8)*20),10);c.setFill(color_rgb(r,r,r));c.draw(panel)	#graphing long set
	global inputData;inputData=trainSet											#first entry of 64 points
dataSetup()


for i in range(l):							#point and matrix creation
	for k in range(net[i]):
		w=[];b=random.randint(-100,0)/500.0
		for j in range(maxNeurons):
			w.append(random.randint(-100,100)/100.0 if j<=net[i-1] else 0)
		p=Point(int(200+400/l+i*180),int(50+600*k/(net[i]-1)))
		dictPos[i,k]=p
		netA[i,k]=0;netW[i,k]=w;netB[i,k]=b
		c=Circle(p,6);c.draw(panel)

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
graph()

def frame(v,graphics):
	global netA;netA[0]=inputData[v]/16.0								#feed-forward using inputs
	for i in range(l-1):
		netA[i+1]=sigmoid(np.dot(netW[i+1],netA[i])+netB[i+1])
	if graphics==1:
		graph()
	y=np.zeros([maxNeurons]);y[int(labels[v])]=1
	cost=np.sum((netA[-1][:10]-y[:10])**2)
	out=np.array([y,netA,netW,netB,cost])
	return out;panel.update()

def backprop(i,n):	#start with n=1
	global gradientA,gradientB,gradientW
	g=frame(i,0)
	for u in range(net[-1]):
		gradientA[-1,u]=2*(netA[-1,u]-g[0][u])					#dC/dA for a whole neuron, which makes propagation easy
		gradientB[-1,u]=2*(netA[-1,u]-g[0][u])*netA[-1,u]*(1-netA[-1,u])
		for j in range(net[-2]):
			gradientW[-1,u,j]=2*(netA[-1,u]-g[0][u])*netA[-1,u]*(1-netA[-1,u])*netA[-2,j]		#dC/dW
	for j in range(net[-2]):							#to make the propagation work
		for r in range(net[-1]):
			gradientA[-2,j]+=gradientA[-1,r]*netA[-1,r]*(1-netA[-1,r])*netW[-1,r,j]

	if l>=3:
		for u in range(net[-1-n]):							#nth layer backwards, computes gA,gW, and gB
			for j in range(net[-2-n]):
				gradientW[-1-n,u,j]=gradientA[-1-n,u]*netA[-1-n,u]*(1-netA[-1-n,u])*netA[-2-n,j]
				gradientB[-1-n,j]=gradientA[-1-n,j]*netA[-1-n,j]*(1-netA[-1-n,j])
		for j in range(net[-2-n]):
			for r in range(net[-1-n]):
				gradientA[-2-n,j]+=gradientA[-1-n,r]*netA[-1-n,r]*(1-netA[-1-n,r])*netW[-1-n,r,j]
	if n<l-2:backprop(i,n+1)
	return [gradientW,gradientB,g[4]]

def train(maxIter,batch):
	global netW,netB,costIndex
	for u in range(int(maxIter/batch)):
		tA=np.zeros([l,maxNeurons]);tW=np.zeros([l,maxNeurons,maxNeurons]);tB=np.zeros([l,maxNeurons]);tC=0
		for i in range(batch):
			p=backprop(i,1)
			tW+=p[0];tB+=p[1];tC+=p[2]
		b=float(batch)
		tW=tW/b;tB=tB/b;tC=tC/b
		print "cost",round(tC,3)
		#np.append(costIndex,tC);np.append(WList,netW);np.append(BList,netB)
		netW=netW-eta*tW;netB=netB-eta*tB
	#print WList[np.argmin(costIndex)],BList[np.argmin(costIndex)]

def classify(start,i):
	for u in range(i):
		g=frame(start+u,1)
		if np.argmax(g[1][-1])==labels[start+u]:
			print "correct, "+str(np.argmax(g[1][-1]))
		else:
			print "wrong, got "+str(np.argmax(g[1][-1]))+" instead of "+str(int(labels[start+u])	)
