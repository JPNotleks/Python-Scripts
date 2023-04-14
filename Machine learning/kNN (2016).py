#My first proper ML project in python, a simple kNN algorithm from 2016 which performs classification on MNIST.


from graphics import *
import numpy
from numpy import *
import operator
import random
from PIL import Image

def prepImg(file):
	img=Image.open(open(file))
	img=img.resize((128,128),Image.ANTIALIAS)
	for i,px in enumerate(img.getdata()):
                x=i%128
                y=i/128
                avg=int((0.299*px[0]+0.587*px[1]+0.114*px[2])/3)*3
                img.putpixel((x,y),(avg,avg,avg))
	add=numpy.zeros((64,256))
	semi=numpy.asarray(list(img.getdata()))
	semi=semi[:,0]
	semi.shape=(128,128)
	zero=numpy.zeros((16,16))
	for i in range(8):
		for k in range(8):
			zero=semi[i*16:(i+1)*16,k*16:(k+1)*16]
			zero=zero.reshape((1,256))
			add[i*8+k]=zero
	for i in range(64):
		add[i]=numpy.sum(add[i])/256
	add=add[:,0]/16
	add=add.astype(int)
	for i in range(64):
		add[i]=16-add[i]
	print add
	index=add.argsort()
	threshold=(add[index[0]]+add[index[-1]])/2
	print threshold
	for i in range(64):
		if add[i]>threshold:
			add[i]=16
		if add[i]<threshold:
			add[i]=0
	add=add.tolist()
	print add
	plot(add)
	img.save("result.jpg")
	return add

def plot(input):
	graph=Image.new("RGB",(8,8),"white")
	for i in range(64):
		c=int(16*input[i])
		graph.putpixel((i%8,i/8),(c,c,c))
	graph=graph.resize((320,320),Image.ANTIALIAS)
	graph.show()
	

def classify(input,k):
	rawData = genfromtxt('./optdigits.tra', delimiter=',')
        trainSet=rawData[:,0:64]
        labels=rawData[:,64]
	if input=="random":
		randomNumber=random.randint(0,3823)
		print "classifying number",randomNumber,"in trainSet"
		input=trainSet[randomNumber]
		plot(input)
	elif input=="image":
		input=prepImg("input.jpg")
	sortedDis=[]
	classVotes=[0,0,0,0,0,0,0,0,0,0]
	for i in range (3823):
		dis=(trainSet[i]-input)**2
		sumDis=dis.sum()
		rootDis=sumDis**0.5
		sortedDis.append(rootDis)
	disIndices=numpy.asarray(sortedDis)
	disIndices=disIndices.argsort()
	for i in range (k):
		labels=numpy.asarray(labels)
		voteLabel=labels[disIndices[i]]
		classVotes[(int(voteLabel))]+=1
	classVotes=numpy.asarray(classVotes)
	classVotes=classVotes.argsort()
	classVotes=classVotes[::-1]
	return classVotes[0]

def accuracyTest(r):
	total=0;success=0
	testData=genfromtxt('./optdigits.tes', delimiter=',')
        testInstances=testData[:,0:64]
	labels=testData[:,64]
	for i in range(r):
		if classify(testInstances[i],1)==labels[i]:
			success+=1
		total+=1.00
		print i
	print success,total
