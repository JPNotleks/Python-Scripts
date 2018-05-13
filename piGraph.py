from graphics import *
import numpy
from numpy import *
import cmath

from PIL import ImageGrab

def saveFile(title):
    ImageGrab.grab((1,50,1001,800)).save(title)

################################### SETUP #####################################

remote=0;xMax=0;yMax=0;xInterval=0;yInterval=0;xGridsize=0;yGridsize=0;yLabelShift=20;xLabels=0;yLabels=0;xOffset=100;yOffset=80
yConstant=0;xConstant=0;origin=Point(100,400)

panel=GraphWin("piGraph by John Skelton 2016-2017",1200,800,autoflush=False)

#data=numpy.array([[0,1,2,3,4,5,6,7,8,9,10],[0,0.2,0.4,0.7,0.85,0.97,1.23,1.35,1.65,1.8,2.0]])
data=numpy.array([[-2.5,-1.5,-0.5,0.5,1.5,2.5],[6.25,2.25,0.25,0.25,2.25,6.25]])

def direct():
	print("parameters : (xMin,xMax,ymin,yMax,xInterval,yInterval,Grid)");peri=raw_input()
	peri=peri.split(",")
	global xMin;xMin=float(peri[0])
	global xMax;xMax=float(peri[1])
	global yMin;yMin=float(peri[2])
	global yMax;yMax=float(peri[3])
	global xInterval;xInterval=float(peri[4])
	global yInterval;yInterval=float(peri[5])
	global grid;grid=int(peri[6])
	global remote;remote=False
	global dmxPoint;dmxPoint=len((peri[1]+".").split('.')[1])
        global dmyPoint;dmyPoint=len((peri[3]+".").split('.')[1])
	setup()

def remote(a,b,c,d):
	global xMax;xMax=a
        global yMax;yMax=b
        global xInterval;xInterval=c
        global yInterval;yInterval=d
	global remote;remote=True
	setup()

def setup():
	global xLabels;xLabels=[]
	global yLabels;yLabels=[]		
	global xConstant;xConstant=float(xMax-xMin)/800
	global yConstant;yConstant=float(yMax-yMin)/640
	global functions;functions=[]
	createLabels()
	
def createLabels():
	if grid==1:
		global origin;origin=Point(-xMin/xConstant+100,yMax/yConstant+80)
		if 80<origin.y<720:
			xaxis=Rectangle(Point(85,origin.y-1),Point(915,origin.y+1));xaxis.setFill("black");xaxis.draw(panel);u=origin.y
                else:
			xaxis=Rectangle(Point(85,399+320*pos(origin.y-400)),Point(915,401+320*pos(origin.y-400)));xaxis.setFill("black")
			xaxis.draw(panel);u=400+320*pos(origin.y-400)
		if 100<origin.x<900:
			yaxis=Rectangle(Point(origin.x-1,65),Point(origin.x+1,735));yaxis.setFill("black");yaxis.draw(panel);v=origin.x
		else:
			yaxis=Rectangle(Point(499+400*pos(origin.x-500),65),Point(501+400*pos(origin.x-500),735))
			yaxis.setFill("black");yaxis.draw(panel);v=500+400*pos(origin.x-500)
		x=Text(Point(940,u),"x");x.draw(panel);y=Text(Point(v,57),"y");y.draw(panel)

		for i in range(int(((xMax-xMin)/xInterval))+1):
                        xP=int(100+xInterval/xConstant*i);r=round(xMin+xInterval*i,dmxPoint)
			if int(r)==0:r=None
                        text=Text(Point(xP+11+len(str(r)),u+9*pos(origin.y-50)),r);text.draw(panel)
			marker=Line(Point(xP,720),Point(xP,80));marker.draw(panel)

		for i in range(int(((yMax-yMin)/yInterval))+1):
                        yP=int(720-yInterval/yConstant*i);r=round(yMin+yInterval*i,dmyPoint)
			if int(r)==0:r=None
                        text=Text(Point(v+pos(origin.x-100)*(2+3*len(str(r))),yP-9),r);text.draw(panel)
                        marker=Line(Point(100,yP),Point(900,yP));marker.draw(panel)


def setGraph(function,ddx,int):
	x=0;r=0.5;xIntercepts=[];yIntercept=0#float(eval(function))
	p=numpy.full(801,str(function),dtype='|S100');idx=numpy.array(range(801))*xConstant+xMin;o=idx;idx=idx.astype('|S20')
	idx=numpy.core.defchararray.add("(",idx);idx=numpy.core.defchararray.add(idx,")")
	p=numpy.core.defchararray.replace(p,'x',idx);p=quickEval(p)

	#for intercept, pos(f,g) changes OR f'(x)=g'(x)

	for i in range(799):
		if yMin<p[i]<yMax:
			graphLine((o[i],p[i]),(o[i+1],p[i+1]),"black")
			k=intersect(p[i],p[i+1],i*xConstant+xMin,(i+1)*xConstant+xMin)
			if k!=None and round(k,4) not in xIntercepts: xIntercepts.append(round(k,4))
			if ddx==1:graphLine((o[i],(p[i+1]-p[i])/xConstant),(o[i+1],(p[i+2]-p[i+1])/xConstant),"blue")
	#	if int==1:graphLine((k1,(400-(r+0.5)*sumPos1-(-r+0.5)*sumNeg1)),(k2,(400-(r+0.5)*sumPos2-(-r+0.5)*sumNeg2)),"red")

	print "x-intercepts: "+str(xIntercepts);print "y-intercept: "+str(yIntercept);functions.append(p);panel.update();print functions

def graphLine(x,y,c):
        line=Line(Point(x[0]/xConstant+origin.x,-x[1]/yConstant+origin.y),Point(y[0]/xConstant+origin.x,-y[1]/yConstant+origin.y))
	line.setFill(c)
        line.draw(panel)

def remoteGraph(r,k):
	K=Point(origin.x+r/xConstant,origin.y-k/yConstant)
	circ=Circle(K,1);circ.draw(panel)
	#l=Line(K,Point(K.x,400));l.draw(panel)
	panel.update()

def intersect(f,g,l,r):     #f(x),f(y),x,y
	f=float(f);g=float(g);l=float(l);r=float(r)
	if round(f,8)==0:return l
        if round(g,8)==0:
		return r
	elif pos(f)!=pos(g): return l+(r-l)/(1-g/f)
	else: return None

#def lhopitale(f,p):
#	try

def cis(x):
	return cos(x)+1j*sin(x)

def pos(x):
	if x>0:
		return 1
	else:
		return -1

def s(x):
        return 1/(1+math.e**(-x))


def base(x,n):
	return color_rgb((x>>8)&0xff,x>>16,x&0xff)
#	if x<n:return color_rgb(0,0,x)
#	if n<x<n**2:a=math.floor(x/n);return color_rgb(0,a,x-a*n)
#	if n**2<x<n**3:a=math.floor(x/n**2);b=math.floor((x-a*n**2)/n);return color_rgb(a,b,x-a*n**2-b*n)

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

	#setGraph()

def point(r,k):
	return Point(r/xConstant+origin.x,-k/yConstant+origin.y)

def clear():
	panel.delete("all");createLabels()

def qEval(a):
	return eval(a)
quickEval=numpy.vectorize(qEval)

def qPlot(x,y,c):
	panel.plot(x,y-100,color_rgb(c%16*15,c%4*63,c%2*30))
	#panel.plot(x,y-100,color_rgb((c>>8)&0xff,c>>16,c&0xff))
quickPlot=numpy.vectorize(qPlot)

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
		for g in range(20):
			t=Text(Point(50,50),"Zoom=%s" %(round(1.0/(0.9**g),3)));t.draw(panel)
			w=1000;z=0.9**g*4.0;x=0.360240443437614363236125244;y=-0.6413130610648031748603750151793020665;n=400
			fM=numpy.zeros([w,w],dtype=complex);kM=numpy.zeros([w,w,3])
			for i in range(w):
				for k in range(w):
					fM[i,k]=complex((i*z/(1.000000000*w)+x-z/2),(k*z/(1.000000000*w)+y-z/2));kM[i,k,0]=i;kM[i,k,1]=k
			init=fM;print fM
	
			for i in range(1,n+1):
				fM=fM*fM+init
				kM[abs(fM)>2,2]=i;init[abs(fM)>2]=0;fM[abs(fM)>2]=0
				print i
			print "graphing"
			kM[:,:,2]=kM[:,:,2]*2**24/(n+1);kM=kM.astype(int)

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
			
			panel.update();print g;saveFile("MandelRes%s.jpg" %(g));panel.delete("all")
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
        		for k in range(1,i):
                		if i%(k)>0:
                        		x=x+1
        			if x==i-2:
                			primes.append(i)
		print primes

		for k in range(800):
			c=Circle(point(k*xConstant,len(primes[0:k])),1);c.draw(panel)

	panel.update()
	
###################################### END ####################################
	
#final=raw_input()
#if final=="save":
#	saveImage=Image(xMax,yMax)
#	panel.draw(saveImage)
#	saveImage.save(title+" ~ piGraph by John Skelton 2016"+".jpg")
#panel.close()