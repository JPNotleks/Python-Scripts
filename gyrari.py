from graphics import *
import numpy as np
import cmath
import math

panel=GraphWin("3D by John Skelton 2017",1400,800,autoflush=False)

def direct():
        print("perimeters : (xMax,yMax,zMax,xRot,yRot,zRot)");peri=raw_input()
        peri=peri.split(",")
        global xMax;xMax=float(peri[0])
        global yMax;yMax=float(peri[1])
        global zMax;zMax=float(peri[2])
        global xRot;xRot=float(peri[3])*math.pi/180
        global yRot;yRot=float(peri[4])*math.pi/180
        global zRot;zRot=float(peri[5])*math.pi/180
 #       global k;k=200
 #       setup()

#def setup():
   #     master=np.zeros((k,k,k))
  #      tf=[xRot,yRot,zRot]
 #       xAxis=Line(Point(500+k*math.cos(xRot)*math.cos(yRot),400+k*math.cos(zRot)*math.sin(yRot)),Point(500-k*math.cos(xRot)*math.cos(yRot),400-k*math.cos(zRot)*math.sin(yRot)));xAxis.draw(panel)
#	xText=Text((Point(500+k*math.cos(xRot)*math.cos(yRot),400+k*math.cos(zRot)*math.sin(yRot))),"x");xText.draw(panel)
#	yAxis=Line(Point(500+k*math.sin(xRot)*math.cos(yRot),400+k*math.cos(zRot)*math.cos(yRot)),Point(500-k*math.sin(xRot)*math.cos(yRot),400-k*math.cos(zRot)*math.cos(yRot)));yAxis.draw(panel)
#	yText=Text(Point(500+k*math.sin(xRot)*math.cos(yRot),400+k*math.cos(zRot)*math.cos(yRot)),"y");yText.draw(panel)
#	zAxis=Line(Point(500+k*math.sin(xRot)*math.sin(yRot),400+k*math.sin(zRot)*math.cos(yRot)),Point(500-k*math.sin(xRot)*math.sin(yRot),400-k*math.sin(zRot)*math.cos(yRot)));zAxis.draw(panel)
#	zText=Text(Point(500+k*math.sin(xRot)*math.sin(yRot),400+k*math.sin(zRot)*math.cos(yRot)),"z");zText.draw(panel)

u=300
res=3
data=np.zeros([u,u],dtype='complex')
X=np.zeros([u,u],dtype='complex')
x=4.0
y=4.0
g=np.array([[1,0],[0.4,0.6]])
for i in range(u):
	for k in range(u):
		data[i,k]=complex((x/u*i)-x/2.0,y/2.0-(y/u*k))
		#X[i,k]=np.dot[data[i,k],g]
std=data;sum=0
#for n in range(1,100):
#        sum+=((-1)**(n-1))*n**(-data)
#sum=sum/(1-2.0**(1-sum))
data=-abs(((((data**2+data)**2+data)**2+data)**2+data)**2+data)+2
#mag=abs(2/((data+1j)*(data-1j)))
#data=math.e**(-data)/data
mag=data

xAxis=Line(Point(70.0,400.0),Point(1270.0,400.0));xAxis.setWidth(4);xAxis.draw(panel)
yAxis=Line(Point(800.0+0.2*(800-602.0),100.0-0.2*(694-100.0)),Point(602-0.2*(800-602.0),694+0.2*(694-100.0)));yAxis.setWidth(4);yAxis.draw(panel)

for i in range(u-1):
        for k in range(u-1):
                p1=Point(300+1000/u*i-k,100+600/u*k)
                p2=Point(300+1000/u*(i+1)-k,100+600/u*k)
                p3=Point(300+1000/u*(i+1)-k-1,100+600/u*(k+1))
                p4=Point(300+1000/u*i-k-1,100+600/u*(k+1))
                pol=Polygon(p1,p2,p3,p4)
		#if i==u/2 and k==0:print Point(300+1000/u*i-k,100+600/u*k)
		#if i==u/2 and k==u-2:print Point(300+1000/u*i-k,100+600/u*k)
                pol.setOutline(color_rgb(0,0,0));pol.draw(panel)

sum=data*0
#for i in range(u-1):
#	for k in range(u-1):
#		if std[i,k].imag<0:
#			for y in range(10):
#				try:sum[i,k]+=data[i,k-y]
#				except error:print i,k
#			for r in range(10-i+u/2):
#				try:sum[i,k]+=data[i+r,k-10]
#				except error:print i,k
#			for e in range(u/2-k+10):
#				try:sum[i,k]+=data[10+u/2,k-10+e]
#				except error:print i,k
#			for j in range(80):
#				try:sum[i,k]+=data[10+u/2+j,u/2]
#				except error:print i,k
#		print sum[i,k]
#	data=sum

#mag=data.imag

for i in range(u-1):
	for k in range(u-1):
		#if data[i,u-k-1].imag<0:mag[i,u-k-1]=-mag[i,u-k-1]
		#if data[i+1,u-k-1].imag<0:mag[i+1,u-k-1]=-mag[i+1,u-k-1]
		#if data[i+1,u-k-2].imag<0:mag[i+1,u-k-2]=-mag[i+1,u-k-2]
		#if data[i,u-k-2].imag<0:mag[i,u-k-2]=-mag[i,u-k-2]
		p1=Point(300+1000/u*i-k,100+600/u*k-25*mag[i,k])
		p2=Point(300+1000/u*(i+1)-k,100+600/u*k-25*mag[i+1,k])
		p3=Point(300+1000/u*(i+1)-k-1,100+600/u*(k+1)-25*mag[i+1,k+1])
		p4=Point(300+1000/u*i-k-1,100+600/u*(k+1)-25*mag[i,k+1])
		pol=Polygon(p1,p2,p3,p4)
		try:
			p=color_rgb(255/(abs(mag[i,k])*2+1),100/(abs(mag[i,k])*2+1),30)
			pol.setOutline(p);pol.setFill(p);pol.draw(panel)
		except TypeError:print "pole encountered"
		#pol=Polygon(Point(200+X[i,k],400+X[i,k]+mag[i,k]),Point(200+res+X[i+res,k],400+X[i+res,k]+mag[i+res,k]),Point(200+res+X[i+res,k+res],400+res+X[i+res,k+res]+mag[i+res,k+res]),Point(200+X[i,k+res],400+res+X[i,k+res]+mag[i,k+res]))
		#pol.setOutline(color_rgb(255/(abs(mag[i,k])*2+1),100/(abs(mag[i,k])*2+1),30));pol.setFill(color_rgb(255/(abs(mag[i,k])*2+1),100/(abs(mag[i,k])*2+1),30));pol.draw(panel)

#l1=Line(Point(200+1000/u*(u/2),50),Point(200+1000/u*(u/2)-u,600/u*(u/2)));l1.draw(panel)
#l2=Line(Point(200-(u/2),50+600/u*(u/2)),Point(200+1000/u*(u/2)-(u/2),50+600/u*(u/2)));l2.draw(panel)
#l3=Line(Point(700-u/4,50),Point(700-u/4,650));l3.draw(panel)

#t1=Text(Point(217+1000-u/2,350),"Re(z)");t1.draw(panel)
#t2=Text(Point(710,35),"Im(z)");t2.draw(panel)
#for i in range(u/2):
#        for k in range(u/2):
#                p1=Point(200+2000/u*i-k,50+1200/u*k)
#                p2=Point(200+2000/u*(i+1)-k,50+1200/u*k)
#                p3=Point(200+2000/u*(i+1)-k-1,50+1200/u*(k+1))
#                p4=Point(200+2000/u*i-k-1,50+1200/u*(k+1))
#                pol=Polygon(p1,p2,p3,p4)
#		pol.setOutline("black");pol.draw(panel)
def save(title):
        panel.postscript(file=str(title+".ps"), colormode='color')

panel.update()
