from graphics import *
import numpy as np
import cmath
import math

panel=GraphWin("3D by John Skelton 2017",1200,800,autoflush=False)

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

u=120
data=np.zeros([u,u],dtype='complex')
x=4.0
y=4.0
for i in range(u):
	for k in range(u):
		data[i,k]=complex((x/u*i)-x/2.0,(y/u*k)-y/2.0)
std=data;print data;sum=0
#for n in range(1,100):
#        sum+=((-1)**(n-1))*n**(-data)
#sum=sum/(1-2.0**(1-sum))
#mag=abs((data**4+2*data**3+data**2+data)**2-data**2)
#mag=np.log(abs(sum))+1
mag=abs(2/((data+1j)*(data-1j)))

for i in range(u-1):
	for k in range(u-1):
		p1=Point(200+1000/u*i-k,100+600/u*k-25*mag[i,u-k-1])
		p2=Point(200+1000/u*(i+1)-k,100+600/u*k-25*mag[i+1,u-k-1])
		p3=Point(200+1000/u*(i+1)-k-1,100+600/u*(k+1)-25*mag[i+1,u-k-2])
		p4=Point(200+1000/u*i-k-1,100+600/u*(k+1)-25*mag[i,u-k-2])
		pol=Polygon(p1,p2,p3,p4)
		pol.setOutline(color_rgb(255/(abs(mag[i,u-k-1])*2+1),100/(abs(mag[i,u-k-1])*2+1),30));pol.setFill(color_rgb(255/(abs(mag[i,u-k-1])*2+1),100/(abs(mag[i,u-k-1])*2+1),30));pol.draw(panel)

#l1=Line(Point(200+1000/u*(u/2),50),Point(200+1000/u*(u/2)-u,600/u*(u/2)));l1.draw(panel)
#l2=Line(Point(200-(u/2),50+600/u*(u/2)),Point(200+1000/u*(u/2)-(u/2),50+600/u*(u/2)));l2.draw(panel)
#l3=Line(Point(700-u/4,50),Point(700-u/4,650));l3.draw(panel)

t1=Text(Point(217+1000-u/2,350),"Re(z)");t1.draw(panel)
t2=Text(Point(710,35),"Im(z)");t2.draw(panel)
#for i in range(u/2):
#        for k in range(u/2):
#                p1=Point(200+2000/u*i-k,50+1200/u*k)
#                p2=Point(200+2000/u*(i+1)-k,50+1200/u*k)
#                p3=Point(200+2000/u*(i+1)-k-1,50+1200/u*(k+1))
#                p4=Point(200+2000/u*i-k-1,50+1200/u*(k+1))
#                pol=Polygon(p1,p2,p3,p4)
#		pol.setOutline("black");pol.draw(panel)
panel.update()
