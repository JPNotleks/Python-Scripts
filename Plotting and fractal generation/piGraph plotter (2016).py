#piGraph is my first large project in python (2016), a fully functional plotter like Desmos.com. It can plot any evaluable
#function including complex-valued functions, it can differentiate and integrate functions numerically, perform complex
#contour integration, and add text or points to an existing graph. Furthermore, it can plot a few custom functions like
#the Riemann zeta function, the prime counting function, the Mandelbrot fractal, the burning ship fractal, and it can
#perform linear regression. Some screenshots are provided in the animations folder.

from graphics import *
import numpy
from numpy import *
import cmath
import math

from PIL import ImageGrab

def saveFile(title):
    ImageGrab.grab((1,50,1001,800)).save(title)

################################### SETUP #####################################

xMax=0;yMax=0;xInterval=0;yInterval=0;xGridsize=0;yGridsize=0;yLabelShift=20;xLabels=0;yLabels=0;xOffset=100;yOffset=80
yConstant=0;xConstant=0;pMatrix=0;globTrans=[500,420]

#data=numpy.array([[0,1,2,3,4,5,6,7,8,9,10],[0,0.2,0.4,0.7,0.85,0.97,1.23,1.35,1.65,1.8,2.0]])
dataSet=numpy.array([[-2.5,-1.5,-0.5,0.5,1.5,2.5],[6.25,2.25,0.25,0.25,2.25,6.25]])

def help():
	print "--available commands--"
	print "init(xMin,xMax,yMin,yMax,xInterval,yInterval,xAxisOn,yAxisOn) creates a new session."
	print "createLabels() redraws axes."
	print "plot(function,resolution,derivative,integral) draws a function of x w/ or w/o d/dx and integral."
	print "complexPlot(function,resolution,mode) plots a complex function. Requires non-standard pMatrix for 3D. Mode can be abs real or imag as a string."
	print "changePMatrix(a,b,c,d) changes the projection matrix basis vectors a,b and c,d."
	print "graphLine([x0,x1],[y0,y1],colour) plots a line."
	print "pointPlot(x,y,size,colour) plots a circle."
	print "edit() then text, line, or exit to manually place text and lines."

def changePMatrix(a,b,c,d):
	global pMatrix;pMatrix=numpy.array([[a,b],[c,d]])
	clear();createLabels()

def init(par0,par1,par2,par3,par4,par5,par6):
	global panel;panel=GraphWin("piGraph by John Skelton 2016-2018",1200,800,autoflush=False)#;panel.setCoords(-500,-400,700,400)
	global xMin;xMin=float(par0)
	global xMax;xMax=float(par1)
	global yMin;yMin=float(par2)
	global yMax;yMax=float(par3)
	global xInterval;xInterval=float(par4)
	global yInterval;yInterval=float(par5)
	global grid;grid=int(par6)
	global dmxPoint;dmxPoint=len((str(par4)+".").split('.')[1])
        global dmyPoint;dmyPoint=len((str(par5)+".").split('.')[1])
	global pMatrix;pMatrix=numpy.array([[1,0],[0,1]])#[[0.7,-0.2],[0.4,0.7]];[[0.2,-0.5],[0.8,0.2]]
	setup()

def setup():
	global xLabels;xLabels=[]
	global yLabels;yLabels=[]		
	global xConstant;xConstant=float(xMax-xMin)/800
	global yConstant;yConstant=float(yMax-yMin)/640
	global functions;functions=[]
	createLabels()

#plane is origin (500+-400,400+-320)

def createLabels():
	global origin;origin=[-(xMax+xMin)/(2*xConstant),-(yMin+yMax)/(2*yConstant)]
	if grid==1:
		if yMin<0 and yMax>0:
                        u=origin[1]
                else:
                        u=320*pos(origin[1])

                if xMin<0 and xMax>0:
                        v=origin[0]
                else:
                        v=400*pos(origin[0])

		if yMin<0 and yMax>0:
			for i in range(int(-xMin/xInterval)+1):
				xP=int(xInterval/xConstant*i)
				if dmxPoint==0:r=-int(xInterval*i)
				else: r=round(-xInterval*i,dmxPoint)
				if r==0:r=None
				text=Text(rawPoint(origin[0]-xP-pos(origin[1])*(2+3*len(str(r))),u+9*pos(origin[1])),r);text.draw(panel)
				marker=Line(rawPoint(origin[0]-xP,-320),rawPoint(origin[0]-xP,320));marker.setFill("grey");marker.draw(panel)
			for i in range(int(xMax/xInterval)+1):
				xP=int(xInterval/xConstant*i)
				if dmxPoint==0:r=int(xInterval*i)
				else: r=round(xInterval*i,dmxPoint)
				if r==0:r=None
				text=Text(rawPoint(origin[0]+xP-pos(origin[1])*(2+3*len(str(r))),u+9*pos(origin[1])),r);text.draw(panel)
				marker=Line(rawPoint(origin[0]+xP,-320),rawPoint(origin[0]+xP,320));marker.setFill("grey");marker.draw(panel)
		else:
			for i in range(int(((xMax-xMin)/xInterval))+1):
				xP=int(xInterval/xConstant*i)
				if dmxPoint==0:r=int(xMin+xInterval*i)
				else: r=round(xInterval*i+xMin,dmxPoint)
				if r==0:r=None
				text=Text(rawPoint(-400+xP-pos(origin[1])*(2+3*len(str(r))),u+9*pos(origin[1])),r);text.draw(panel)
				marker=Line(rawPoint(-400+xP,-320),rawPoint(-400+xP,320));marker.setFill("grey");marker.draw(panel)

		if xMin<0 and xMax>0:
			for i in range(int(-yMin/yInterval)+1):
				yP=int(yInterval/yConstant*i)
				if dmyPoint==0:r=-int(yInterval*i)
				else: r=round(-yInterval*i,dmyPoint)
				if r==0:r=None
				text=Text(rawPoint(v+2+4*len(str(r)),origin[1]-yP-7*pos(origin[0])),r);text.draw(panel)
				marker=Line(rawPoint(-400,origin[1]-yP),rawPoint(400,origin[1]-yP));marker.setFill("grey");marker.draw(panel)
			for i in range(int(yMax/yInterval)+1):
				yP=int(yInterval/yConstant*i)
				if dmyPoint==0:r=int(yInterval*i)
				else: r=round(yInterval*i,dmyPoint)
				if r==0:r=None
				text=Text(rawPoint(v+2+4*len(str(r)),origin[1]+yP-7*pos(origin[0])),r);text.draw(panel)
				marker=Line(rawPoint(-400,origin[1]+yP),rawPoint(400,origin[1]+yP));marker.setFill("grey");marker.draw(panel)
		else:
			for i in range(int(((yMax-yMin)/yInterval))+1):
				yP=int(yInterval/yConstant*i)
				if dmyPoint==0:r=int(yMin+yInterval*i)
				else: r=round(yMin+yInterval*i,dmyPoint)
				if r==0:r=None
				text=Text(rawPoint(v+pos(origin[1])*(2+4*len(str(r))),-320+yP-9*pos(origin[1])),r);text.draw(panel)
				marker=Line(rawPoint(-400,-320+yP),rawPoint(400,-320+yP));marker.setFill("grey");marker.draw(panel)

		if yMin<0 and yMax>0:
                        xaxis=Line(rawPoint(-415,origin[1]),rawPoint(415,origin[1]))
                        xaxis.setWidth(3);xaxis.setFill("black");xaxis.draw(panel);u=origin[1]
                else:
                        xaxis=Line(rawPoint(-415,320*pos(origin[1])),rawPoint(415,320*pos(origin[1])))
                        xaxis.setWidth(3);xaxis.setFill("black");xaxis.draw(panel);u=320*pos(origin[1])

                if xMin<0 and xMax>0:
                        yaxis=Line(rawPoint(origin[0],-335),rawPoint(origin[0],335))
                        yaxis.setWidth(3);yaxis.setFill("black");yaxis.draw(panel);v=origin[0]
                else:
                        yaxis=Line(rawPoint(400*pos(origin[0]),-335),rawPoint(400*pos(origin[0]),335))
                        yaxis.setWidth(3);yaxis.setFill("black");yaxis.draw(panel);v=400*pos(origin[0])

def plot(function,res,derivative,integral):
	res=int(res)
	x=0;r=0.5;xIntercepts=[];localExtrema=[]
	try:yIntercept=float(eval(function))
	except:yIntercept="{}"

	p=numpy.full(res*800+1,str(function),dtype='|S100');idx=numpy.array(range(res*800+1))*xConstant/res+xMin;o=idx;idx=idx.astype('|S100')
	idx=numpy.core.defchararray.add("(",idx);idx=numpy.core.defchararray.add(idx,")")
	p=numpy.core.defchararray.replace(p,'x',idx);p=quickEval(p)

	for i in range(799):
		j=res*i
		if yMin<p[j]<yMax and yMin<p[j+1]<yMax:
			graphLine((o[j],p[j]),(o[j+res],p[j+res]),"black")
		for u in range(res):
			h=intersect(p[j+u],p[j+u+1],(j+u)*xConstant/res+xMin,(j+u+1)*xConstant/res+xMin)
			if h!=None and round(h,4) not in xIntercepts: xIntercepts.append(round(h,4))	
	if derivative==1:
		k=ddx(p)
		for i in range(798):
			j=res*i
			#if yMin<k[j]<yMax and yMin<k[j+1]<yMax:
			graphLine((o[j],res*k[j]),(o[j+res],res*k[j+res]),"blue")
			for u in range(res):
        	               h=intersect(k[j+u],k[j+u+1],(j+u)*xConstant/res+xMin,(j+u+1)*xConstant/res+xMin)
                               if h!=None and round(h,4) not in localExtrema: localExtrema.append(round(h,4))

	if integral!=0:
		l=(integral-xMin)*res/xConstant
		for i in range((integral/xConstant),799):
			j=l+res*i;graphLine((o[j],xConstant*numpy.sum(p[l:j])/res),(o[j+res],xConstant*numpy.sum(p[l:(j+res)])/res),"red")

	print "x-intercepts: "+str(xIntercepts);print "y-intercept: "+str(yIntercept);print "local extrema: "+str(localExtrema);functions.append(p);panel.update()

def complexPlot(function,res,mode):
	u=int(res)*100
	z=numpy.array([[[complex(round((xMax-xMin)/u*i+xMin,5),round((yMax-yMin)/u*l+yMin,5))] for i in range(u+1)] for l in range(u+1)])
	f=eval(function)
	if mode=="abs":data=abs(f)
	if mode=="real":data=f.real
	if mode=="imag":data=f.imag
	if (pMatrix==numpy.array([[1,0],[0,1]])).all():
		c=0
	else:
		c=1
	for i in range(1,u+1):
	        for k in range(1,u+1):
			if data[u-i,u-k]!=inf and data[u-i,u-k+1]!=inf and data[u-i+1,u-k+1]!=inf and data[u-i+1,u-k]!=inf:
        	        	p1=complexPoint(z[u-i,u-k][0].real,z[u-i,u-k][0].imag,c*data[u-i,u-k])
        	        	p2=complexPoint(z[u-i,u-k+1][0].real,z[u-i,u-k+1][0].imag,c*data[u-i,u-k+1])
        	        	p3=complexPoint(z[u-i+1,u-k+1][0].real,z[u-i+1,u-k+1][0].imag,c*data[u-i+1,u-k+1])
        	        	p4=complexPoint(z[u-i+1,u-k][0].real,z[u-i+1,u-k][0].imag,c*data[u-i+1,u-k])
				if not math.isnan(f[u-i,u-k][0].real) and not math.isnan(f[u-i,u-k][0].imag):
					pol=Polygon(p1,p2,p3,p4);pol.setFill(rainbow((cmath.phase(f[u-i,u-k][0])/math.pi+1)/2*255))
					pol.setOutline(rainbow((cmath.phase(f[u-i,u-k][0])/math.pi+1)/2*255));pol.draw(panel)

def contourIntegral(function,bound,k):
        p=numpy.full(3201,str(function),dtype='|S100');idx=numpy.array(range(3201))**bound[1]+bound[0];o=idx;idx=idx.astype('|S20')
        p=numpy.core.defchararray.replace(p,'z',idx);p=quickEval(p)

	for i in range(3199):
                graphLine((numpy.sum(p[0:i].real)*xConstant+k.real,numpy.sum(p[0:i].imag)*xConstant+k.imag),(numpy.sum(p[0:i+1].real)*xConstant+k.real,numpy.sum(p[0:i+1].imag)*xConstant+k.imag),"red")


def ddx(k):
	return (k[1:-1]-k[0:-2])/xConstant

def graphLine(x,y,c):
        line=Line(point(x[0],x[1]),point(y[0],y[1]))
	line.setFill(c)
        line.draw(panel)

def pointPlot(x,y,s,c):
	circ=Circle(point(x,y),s)
	circ.setFill(c)
	circ.draw(panel)

def intersect(f,g,l,r):     #f(x),f(y),x,y      for intercept, pos(f,g) changes OR f'(x)=g'(x) and f-g~0
	f=float(f);g=float(g);l=float(l);r=float(r)
	if round(f,8)==0:return l
        if round(g,8)==0:
		return r
	elif pos(f)!=pos(g): return l+(r-l)/(1-g/f)
	else: return None

#def lhopitale(f,g,p):
#	differentiate f and g numerically, then divide (perhaps regression?)

def cis(x):
	return cos(x)+1j*sin(x)

def pos(x):
	if x>0:
		return 1
	else:
		return -1

def movie(k,s,e):
	for i in range(s,e):
		f(k);r=Rectangle(Point(300,20),Point(310,30))
		r.setFill("white");r.draw(panel)
		t=Text(Point(300,20),"%s%d"%("n=",i));t.draw(panel)
		#panel.save("%s %d/%d%s" % (k,s,e,".jpg"))
		saveFile("%s %d/%d%s" % (k,s,e,".jpg"))

def leastSquares(f,a,g):
	for i in range(data[0,:].size):
		c=Circle(point(data[:,i][0],data[:,i][1]),3);c.draw(panel)

	#plot()

def point(r,k):
	return rawPoint(origin[0]+r/xConstant,origin[1]+k/yConstant)

def rawPoint(r,k):
	#g=numpy.dot([r,k],pMatrix)
	#return Point(g[0]+globTrans[0],g[1]+globTrans[1])
	return Point(r+500,k+420)
qRawPoint=numpy.vectorize(rawPoint)

def complexPoint(r,k,v):
	g=numpy.dot([origin[0]+r/xConstant,origin[1]+k/yConstant],pMatrix)
        return Point(g[0]+globTrans[0],g[1]+v+globTrans[1])	

def clear():
	panel.delete("all");createLabels()

def qEval(a):
	try: return eval(a)
	except:return nan
quickEval=numpy.vectorize(qEval)

def qPlot(x,y,c):
	k=Point(x+globTrans[0],y+globTrans[1])
	k.setFill(rainbow(c))
	#color_rgb(c%16*15,c%4*63,c%2*30))
	k.draw(panel)
	#color_rgb((c>>8)&0xff,c>>16,c&0xff))
quickPlot=numpy.vectorize(qPlot)

def rainbow(x):
	if x>255:x=x%255
	if x==0:
		r=0;g=0;b=0
        if 0<x<255/6.0:
                r=255;g=6*x;b=0
        if 255/6.0<=x<2*255/6.0:
                r=255-6*(x-255/6.0);g=255;b=0
        if 2*255/6.0<=x<3*255/6.0:
                r=0;g=255;b=6*(x-2*255/6.0)
        if 3*255/6.0<=x<4*255/6.0:
                r=0;g=255-6*(x-3*255/6.0);b=255
        if 4*255/6.0<=x<=5*255/6.0:
                r=6*(x-4*255/6.0);g=0;b=255
	if 5*255/6.0<=x<=255:
                r=255;g=0;b=255-6*(x-5*255/6.0)
        return color_rgb(r,g,b)

def barGraph(data):
	for i in range(len(data[1])):
		rect=Rectangle(point(data[0][i]-0.5,0),point(data[0][i]+0.5,data[1][i]));rect.setFill("blue");rect.draw(panel)

def lineGraph(data):
	for i in range(len(data[1])-1):
		l=Line(point(data[0,i],data[1,i]),point(data[0,i+1],data[1,i+1]));l.draw(panel)

def s(x):
        y=numpy.piecewise(x,[x<-5,-5<=x<=5,x>5],[0,1/(1+math.e**(-x)),1])
        return y*(1-y)
sigmoid=numpy.vectorize(s)

#################################### MAIN ###################################

function=0
functionStore=0

def edit():
	f=raw_input()
	if f=="text":
		p=panel.getMouse()
		s=raw_input();t=Text(p,"%s" %(s));t.draw(panel)
	if f=="line":
		p=panel.getMouse();c=Circle(p,2);c.draw(panel)
		q=panel.getMouse();c.undraw()
		l=Line(p,q);l.draw(panel)
	if f!="exit": edit()

def f(function):
	global yLabelShift
	global functionStore

	if function=="mandelbrot":
		#t=Text(Point(50,50),"Zoom=%s" %(round(1.0/(0.9**g),3)));t.draw(panel)
		n=100
		kM=numpy.zeros([640,800,3],dtype='int')
		fM=numpy.tile(numpy.linspace(xMin,xMax,num=800,dtype='complex64'),(640,1))+numpy.transpose(numpy.tile((0+1j)*numpy.linspace(yMin,yMax,num=640,dtype='complex64'),(800,1)))
		kM[:,:,0]=numpy.round(fM.real/xConstant+origin[0]);kM[:,:,1]=numpy.round(fM.imag/yConstant+origin[1])
		init=fM;print kM
	
		for i in range(1,n+1):
			fM=fM**2+init
			kM[abs(fM)>2,2]=i;init[abs(fM)>2]=0;fM[abs(fM)>2]=0
			print i
		print "graphing"
		#kM[:,:,2]=kM[:,:,2]*2**24/(n+1);kM=kM.astype(int)

		kM[:,:,2]=510*s(kM[:,:,2]/32)-255

		#r=numpy.zeros([1600])
		#for i in range(w):
		#	for k in range(w):
		#		x=(log(abs(fM[i,k]))/log(2))/n
		#		y=math.floor(x*800.0)
		#		if -800<y<800:r[y+800]+=1
		#for i in range(1600):
		#	graphLine(((i-800.00)/800*n,0),((i-800.00)/800*n+xConstant,r[i]),"red")
		#	#print (i-800.00)/800*n,(i-800.00)/800*n+xConstant,r[i]
		quickPlot(kM[:,:,0],kM[:,:,1],kM[:,:,2])

		#for i in range(w):
		#	for k in range(w):
		#		panel.plot(init.real[i,k]/xConstant+origin[0],init[i,k].imag/yConstant+origin[1],rainbow(kM[i,k,2]))

		panel.update()
		#print g;saveFile("MandelRes%s.jpg" %(g));panel.delete("all")
		#	z=0+0j
                #        c=-0.5+1j
                #        for n in range(g):
                #               z=z**2+c
                #       c=Circle(Point(2*z.real/xConstant+origin.x,-2*z.imag/(float(yMax-yMin)/320)+origin.y),4);c.setFill("black");c.draw(panel);print z.real/xConstant+origin.x,z.imag/(float(yMax-yMin)/320)+origin.y
		#createLabels()`

	if function=="mandelpoop":
		for n in range(100,110):
			u=10000
			for i in range(2,2*u):
                	        z=((i)*1.00000/u-2.5)
                	        zC=z
                	        for k in range(n):
					if abs(z)<10:z=z**2+zC
                	        
				w=((i-1)*1.00000/u-2.5)
                	        wC=w
                	        for k in range(n):
                	                if abs(w)<10:w=w**2+wC
                	        graphLine((zC,z),(wC,w),"black")
			panel.update()

	if function=="oliver": #single variable regression
		input=numpy.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99])
		output=numpy.array([86,135,179,224,242,244,245,270,309,436,528,528,599,759,844,964,1048,1201,1617,1835,2225,3052,3944,4366,5325,6242,7157,8011,8973,9911,13676,13015,14068,15113,15901,17111,17908,18569,19463,20171,20712,21261,21689,22057,22460,22859,23218,23694,23934,24247,24666,24872,25178,25515,25791,26101,26298,26648,26763,26979,27055,27173,27275,27352,27479,27540,27585,27642,27705,27748,27890,27948,27982,28051,28102,28160,28245,28319,28408,28421,28466,28504,28546,28581,28599,28598,28601,28601,28601,28604,28601,28601,28601,28601,28602,28603,28603,28603,28603,28603])
		for i in range(800):
			k1=0.2/800*i
			reg=[0,0,0,0,0,0]
			for u in range(3):
				k=0.2/800*(i+u)
				reg[u+3]=k
				reg[u]=(86*28603)/((28603-86)*math.e**(-k*input)+86)
				reg[u]=(reg[u]-output)**2
				reg[u]=math.log(numpy.sum(reg[u]))
			graphLine([reg[3],reg[0]],[reg[4],reg[1]],"blue")
			print intersect(reg[1]-reg[0],reg[2]-reg[1],reg[4],reg[3])
			#print reg[1]-reg[0],reg[2]-reg[1]

	if function=="complex":
		map=numpy.zeros([500,100],dtype=complex);cmap=numpy.zeros([500,100],dtype=complex)
		for i in range(-250,250):
                	for k in range(-25,25):
				map[i+250,k+25]=complex(1.0000*i*xConstant,1.0000*k/320*yMax)
                                #c=map[i+400,k+400]**2
				#p=Line(Point(500+i*20,400+k*32),Point(500+c.real*20,400+c.imag*32));p.draw(panel)
		cmap=map**2
		for i in range(-250,250):
                        for k in range(-25,25):
				c=cmap[i+250,k+25]
				m=map[i+250,k+25]
				p=Circle(Point(c.real*1000,c.imag*1000),1);p.draw(panel)
                                #p=Line(Point(m.real*1200,m.imag*1200),Point(c.real*1200,c.imag*1200));p.setFill(color_rgb(255/(abs(m-c)**2+1),200,30*(cmath.phase(c))**2));p.draw(panel)
		panel.update()

	if function=="zeta":
		for g in range(1):
			createLabels()
			t=Text(Point(50,50),"Iteration %d" %(g+1));t.draw(panel)
			for i in range(50*int(xMax)):
				z=complex(0.5,(i)/50.00000);zSum=0;zCSum=0;b=z.imag
			#	for n in range(1,1000):
			#		zSum+=((-1)**(n-1))*n**(-z)
                	 #               zCSum+=(-1)**(n)*(1j*sin(b*math.log(n))-cos(b*math.log(n)))/(n**0.5)
			#	zSum=zSum/(1-2**(1.0-z));zCSum=zCSum/(1-2**(1.0-z))
	#
				w=complex(0.5,(i+1)/50.00000);wSum=0;wCSum=0;v=w.imag
	#			for n in range(1,1000):
	 #                               wSum+=((-1)**(n-1))*n**(-w)
	#				wCSum+=(-1)**(n)*(1j*sin(v*math.log(n))-cos(v*math.log(n)))/(n**0.5)
	 #                       wSum=wSum/(1-2**(1.0-w));wCSum=wCSum/(1-2**(1.0-w))
	#			for o in range(4,6,2):
	#				c=0.0
         #                       	for k in range(500):
          #                              	it=((-1)**k)*(log(k+1)**o)/((k+1)**0.5*math.factorial(o))
	#					c+=it#;print int(it)
	#					poo=Circle(point(k,c),2)
	#					poo.draw(panel)
         #                       	c=c/math.factorial(o)
	#				zCSum+=c*b**o
	#				wCSum+=c*v**o
				#print zCSum
				#graphLine((zSum.real,-zSum.imag),(wSum.real,-wSum.imag),"blue")
				#graphLine((zCSum.real,zCSum.imag),(wCSum.real,wCSum.imag),"red")
				#graphLine((i/50,zCSum.real),(i/50+xConstant,wCSum.real),"blue")
				#graphLine((i/50,zCSum.imag),(i/50+xConstant,wCSum.imag),"red")
			for r in range(1,100):
				n=r/5.0
				t=(1)**(n)*(1j*sin(14.134725*math.log(n))-cos(14.134725*math.log(n)))/(n**0.5)#/(1-2**(0.5+14.134725j))
				y=(1)**(n+1)*(1j*sin(14.134725*math.log(n+1))-cos(14.134725*math.log(n+1)))/((n+1)**0.5)#/(1-2**(0.5+14.134725j))	
				graphLine((t.real,t.imag),(y.real,y.imag),"black")#;c.setFill("black");c.draw(panel)
			panel.update()#;saveFile("ZetaTest%s.jpg" %(g))#;panel.delete("all")
		panel.update()
		#panel.delete("all")

	if function=="factors":
		for i in range(1,1000):
			sum=0
			for k in range(1,i):
				if i%k==0:sum+=1
			c=Circle(Point(500+i*0.4,400-sum*300/yMax),2);c.draw(panel)

	if function=="fieldLines":
		field=numpy.zeros([800,800],dtype='complex')
		for i in range(800):
                                for k in range(800):
                                        field[i,k]=complex(i*xConstant+xMin,k*xConstant+yMin)
		field=abs(field)#**2+field
		for i in range(11):
			def f(x):return(int(1/xConstant*(x*math.tan(-1+i/5.0)*xConstant)))
			for x in range(100):
				graphLine([field[400+x,400+f(x)].real,field[400+x,400+f(x)].imag],[field[401+x,400+f(x+1)].real,field[401+x,400+f(x+1)].imag],"red")
				graphLine([field[401-x,400+f(-x)].real,field[401-x,400+f(-x)].imag],[field[400-x,400+f(-x-1)].real,field[400-x,400+f(-x-1)].imag],"red")
			#def g(y):return(int(1/yConstant*(i/4.0-2+(0*yConstant))))
                        #for y in range(399):
                        #        graphLine([field[400+f(y),400+y].real,field[400+f(y),400+y].imag],[field[400+f(y),401+y].real,field[400+f(y),401+y].imag],"red")
                        #        graphLine([field[400+f(-y),401-y].real,field[400+f(-y),401-y].imag],[field[400+f(-y-1),400-y].real,field[400+f(-y-1),400-y].imag],"red")



	if function=="x^x":
		for i in range(1,400):
			x=float(i*xConstant)
			y1=eval("x**x")/(float(yMax)/320);y2=eval("(1/x)**x")/(float(yMax)/320);y3=eval("(1/x)**x*-1")/(float(yMax)/320)
		
			x=float((i+1)*xConstant)
			y11=eval("x**x")/(float(yMax)/320);y22=eval("(1/x)**x")/(float(yMax)/320);y33=eval("(1/x)**x*-1")/(float(yMax)/320)
			
			if -320<y1<320:graphLine((i,-y1),(1+i,-y11),"black")
                        if -320<y2<320:graphLine((1-i,400-y2),(-i,400-y22),"black")
			if -320<y3<320:graphLine((501-i,400-y3),(500-i,400-y33),"black")

			x=xConstant*i
                        y1=0+0j;y1=x**(-x)*cis(-x*math.pi)/(float(yMax)/320)
                        x=xConstant*(i+1)
                        y11=0+0j;y11=x**(-x)*cis(-x*math.pi)/(float(yMax)/320)

                        if -320<y1<320:
                                y2=int(imag(y1));y22=int(imag(y11))
                                l=Line(Point(500-i,400-y22),Point(501-i,400-y2));l.setFill("red");l.draw(panel)
                        if -320<y11<320:
                                y3=int(real(y1));y33=int(real(y11))
                                l=Line(Point(500-i,400-y33),Point(501-i,400-y3));l.setFill("blue");l.draw(panel)
			
	if function=="integral":
		j=float(raw_input())
		k=float(raw_input())
		sum=0
		for i in range(400):
			if i>j*400/xMax and i<k*400/xMax:
				x=float(i*xConstant)
				sum=sum+eval(functionStore)
                        if -i>j*400/xMax and -i<k*400/xMax:
				x=float(-i*xConstant)
                                sum=sum+eval(functionStore)
		sum=sum*xConstant
		print "integral from "+str(j)+" to "+str(k)+" is "+str(sum)

	if function=="pi(x)":
		primes=[]
		for i in range(int(xMax)):
			x=0
        		for k in range(1,i):
                		if i%(k)>0:
                        		x=x+1
        		if x==i-2:
                		primes.append(1)
			else: primes.append(0)
			print i

		for k in range(int(xMax)):
			if primes[k]==1:
				graphLine([k,numpy.sum(primes[0:k])],[k,numpy.sum(primes[0:k])+1],"red")
			graphLine([k-1,numpy.sum(primes[0:k])],[k,numpy.sum(primes[0:k])],"red")

		#for k in range(800):
		#	c=Circle(point(k*xConstant,len(primes[0:k])),1);c.draw(panel)
	panel.update()
	
###################################### END ####################################

def save(title):
	panel.postscript(file=str(title+".ps"), colormode='color')	
#final=raw_input()
#if final=="save":
#	saveImage=Image(xMax,yMax)
#	panel.draw(saveImage)
#	saveImage.save(title+" ~ piGraph by John Skelton 2016"+".jpg")
#panel.close()
