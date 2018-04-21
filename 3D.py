from graphics import *
import numpy as np
import math

panel=GraphWin("3D by John Skelton 2017",1000,800,autoflush=True)

def direct():
	print("perimeters : (xMax,yMax,zMax,xRot,yRot,zRot)");peri=raw_input()
        peri=peri.split(",")
        global xMax;xMax=float(peri[0])
	global yMax;yMax=float(peri[1])
	global zMax;zMax=float(peri[2])
	global xRot;zRot=float(peri[3])
	global yRot;zRot=float(peri[4])
	global zRot;zRot=float(peri[5])
	global k;k=400
	setup()

def setup():
	master=np.zeros((k,k,k))
	tf=(math.cos(xRot),math.cos(yRot),math.cos(zRot))
	xAxis=Line(Point(-k*tf[1]),Point(k*tf[1]));xAxis.draw
	yAxis=Line(Point(-k*tf[2]),Point(k*tf[2]));yAxis.draw
	zAxis=Line(Point(-k*tf[3]),Point(k*tf[3]));zAxis.draw

