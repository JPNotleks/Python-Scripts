#A script written to plot a custom function for a thesis.

from graphics import *
import cmath
import math
import numpy as np

def rainbow(x):
        if x>255:x=x%255
        if 0<=x<255/6.0:
                r=255;g=6*x;b=0
        if 255/6.0<=x<2*255/6.0:
                r=255-6*(x-255/6.0);g=255;b=0
        if 2*255/6.0<=x<3*255/6.0:
                r=0;g=255;b=6*(x-2*255/6.0)
        if 3*255/6.0<=x<4*255/6.0:
                r=0;g=255-6*(x-3*255/6.0);b=255
        if 4*255/6.0<=x<=6*255/6.0:
                r=6*(x-4*255/6.0);g=0;b=255
        if 5*255/6.0<=x<=255:
                r=255;g=0;b=255-6*(x-5*255/6.0)
        return color_rgb(r,g,b)

panel=GraphWin("IAtest Graphics",1200,800,autoflush=False)
data=[]

def text():
	p=panel.getMouse()
	s=raw_input();t=Text(p,"%s" %(s));t.draw(panel)

def cis(x):
	return math.cos(x)+1j*math.sin(x)

for i in range(600):
	data.append((cis(i*2*math.pi/600)))
data=np.array(data)
print np.sum(data)

k=np.array([[0.4,0.6],[0,1]]) #standard [[0.4,0.6],[0,1]]
xIndex1=np.dot([-1,0],k)
xIndex2=np.dot([1,0],k)
yIndex1=np.dot([0,-1],k)
yIndex2=np.dot([0,1],k)

xAxis=Line(Point(200+200*xIndex1[0],400-200*xIndex1[1]),Point(200+200*xIndex2[0],400-200*xIndex2[1]));xAxis.draw(panel)
yAxis=Line(Point(200+200*yIndex1[0],400-200*yIndex1[1]),Point(200+200*yIndex2[0],400-200*yIndex2[1]));yAxis.draw(panel)
yTop=Line(Point(200+200*yIndex2[0],400-200*yIndex2[1]),Point(800+200*yIndex2[0],400-200*yIndex2[1]));yTop.draw(panel)
yBot=Line(Point(200+200*yIndex1[0],400-200*yIndex1[1]),Point(800+200*yIndex1[0],400-200*yIndex1[1]));yBot.draw(panel)
xTop=Line(Point(200+200*xIndex2[0],400-200*xIndex2[1]),Point(800+200*xIndex2[0],400-200*xIndex2[1]));xTop.draw(panel)
xBot=Line(Point(200+200*xIndex1[0],400-200*xIndex1[1]),Point(800+200*xIndex1[0],400-200*xIndex1[1]));xBot.draw(panel)
lAxis=Line(Point(200,400),Point(800,400));lAxis.draw(panel)

for i in range(599):
	x1=np.array([data[i].real,data[i].imag])
	x2=np.array([data[i+1].real,data[i+1].imag])
	x1=np.dot(x1,k)*200
	x2=np.dot(x2,k)*200
	l=Polygon(Point(200+i,400),Point(200+i+x1[0],400-x1[1]),Point(201+i+x2[0],400-x2[1]))
	#l=Polygon(Point(200,400),Point(200+x1[0],400-x1[1]),Point(201+x2[0],400-x2[1]))
	c=rainbow(((cmath.phase(data[i])/math.pi+1)/2*255))
	l.setFill(c);l.setOutline(c);l.draw(panel)
	l=Line(Point(200+i+x1[0],400-x1[1]),Point(201+i+x2[0],400-x2[1]));l.draw(panel)

xBot=Line(Point(200+200*xIndex1[0],400-200*xIndex1[1]),Point(800+200*xIndex1[0],400-200*xIndex1[1]));xBot.draw(panel)
xAxis=Line(Point(200+200*xIndex1[0],400-200*xIndex1[1]),Point(200+200*xIndex2[0],400-200*xIndex2[1]));xAxis.draw(panel)
yAxis=Line(Point(200+200*yIndex1[0],400-200*yIndex1[1]),Point(200+200*yIndex2[0],400-200*yIndex2[1]));yAxis.draw(panel)
