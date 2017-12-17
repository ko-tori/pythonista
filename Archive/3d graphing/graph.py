from scene import *
from math import *

axes=True
circle=0#True

def distance(p1,p2):
	return ((p1.x-p2.x)**2+(p1.y-p2.y)**2)**.5

class Param(Scene):
	def setup(self):
		x=[-300,300,0,0,0,0]
		y=[0,0,-300,300,0,0]
		z=[0,0,0,0,-300,300]
		self.data=[[0,x,y,z,0]] if axes else []
		self.v=[0,0,0]
		self.off=[0,0]
		self.sc=15
		#Heart Shape
		#self.gparam1(['16*sin(t)**3','13*cos(t)-5*cos(2*t)-2*cos(3*t)-cos(4*t)','0'], 0, 2*pi, 20, color=(1,0,1,.8))
		#self.gparam1(['16*sin(t)**3','13*cos(t)-5*cos(2*t)-2*cos(3*t)-cos(4*t)','10*sin(t)-5*cos(t)'], 0, 2*pi, 20, color=(1,0,1,.8))
		#Trefoil Knot
		#self.gparam1(['sin(t)+2*sin(2*t)','cos(t)-2*cos(2*t)','-sin(3*t)'],0,2*pi,30/pi)
		#Random Example
		#self.gparam1()
		#self.graphz('x+y',(-5,5)*2,2)
		#Paraboloid
		#self.graphz('(x**2+y**2)/5',(-5,5)*2,2)
		#Mobius Strip
		#self.gparam2(['(7+s*cos(t/2))*cos(t)','(7+s*cos(t/2))*sin(t)','s*sin(t/2)'],(0,2*pi),(-3,3),30/pi,.5)
		#Mobius Strip 2
		#self.gparam2(['(4+s*cos(t/2))*cos(t)','(4+s*cos(t/2))*sin(t)','s*sin(t/2)'],(0,2*pi),(-8,8),30/pi,.5)
		#'Kiss Surface'
		#self.gparam2(['5*t**2*sqrt((1-t)/2)*cos(s)','5*t**2*sqrt((1-t)/2)*sin(s)','5*t'],(-pi,2*pi),(-pi,2*pi),60/pi,10/pi)
		#Torus
		self.gparam2(['(2+cos(t))*cos(s)*2','(2+cos(t))*sin(s)*2','sin(t)*2'],(0,2*pi),(0,2*pi),7.5/pi,18/pi)
		#Corkscrew Surface
		#self.gparam2(['5*cos(t)*cos(s)','5*sin(t)*cos(s)','5*sin(t)+10*s/pi'],(0,2*pi),(-pi,pi-.1),10/pi,15/pi)
		#poo
		#self.gparam2(['(1-s)*(3+cos(t))*cos(4*pi*s)','(1-s)*(3+cos(t))*sin(4*pi*s)','3*s+(1-s)*sin(t)-8'],(0,8),(1,3),2, 32)
		#self.gparam2(['s*sin(t)','s*cos(t)','2-s*cos(t)'],(0,2*pi),(0,2),30/pi,1)
		#self.graphz('x/y',px=1,py=2)

	def graphz(self, z, r=(-8,8)*2, px=1, py=None):
		xmin,xmax,ymin,ymax=r
		if py is None:
			py=px
		px*=1.
		py*=1.
		lx=[]
		ly=[]
		lz=[]
		x=xmin
		while x<=xmax:
			y=ymin
			while y<=ymax:
				temp=x,y
				try:
					lz.append(eval(z))
				except:
					x=''
					y=''
					lz.append('')
				lx.append(x)
				ly.append(y)
				x,y=temp
				y+=1/py
			x+=1/px
		self.data.append([2,lx,ly,lz,int((ymax-ymin)*py+1)])
	
	def gparam1(self, r=['sin(2*t)','sin(3*t)','cos(5*t)'],min=-pi,max=pi,p=60/pi, color=(0,0,0,.3)):
		p*=1.
		x,y,z=[],[],[]
		t=min-1/p
		while t<=max:
			t+=1/p
			try:
				x.append(eval(r[0]))
			except:
				x.append('')
			try:
				y.append(eval(r[1]))
			except:
				y.append('')
			try:
				z.append(eval(r[2]))
			except:
				z.append('')
		self.data.append([1,x,y,z,color])
		
	def gparam2(self, r, tr, sr, pt, ps=None):
		tmin,tmax,smin,smax=tr+sr
		if ps is None:
			ps=pt
		pt*=1.
		ps*=1.
		x=[]
		y=[]
		z=[]
		t=tmin
		while t<=tmax:
			s=smin
			while s<=smax:
				try:
					x.append(eval(r[0]))
				except:
					x.append('')
				try:
					y.append(eval(r[1]))
				except:
					y.append('')
				try:
					z.append(eval(r[2]))
				except:
					z.append('')
				s+=1/ps
			t+=1/pt
		self.data.append([2,x,y,z,int((smax-smin)*ps+1)])
		
	def draw(self):
		background(*(1,)*3)
		translate(*self.bounds.center())
		background(1,1,1)
		fn=0
		stroke(0,0,0)
		if circle:ellipse(-303,-303,606,606)
		for mode,x,y,z,o in self.data:
			if mode>0:
				x,y,z=([i*self.sc if i!='' else '' for i in j] for j in (x,y,z))
			stroke_weight(2)
			if mode==-1:
				stroke(0,0,0,.6)
				for i,j in zip(o[::2],o[1::2]):
					line(x[i],y[i],x[j],y[j])
			if mode==0:
				stroke(1,0,0,.5)
				line(x[0],y[0],x[1],y[1])
				stroke(0,1,0,.5)
				line(x[2],y[2],x[3],y[3])
				stroke(0,0,1,.5)
				line(x[4],y[4],x[5],y[5])
				tint(1,0,0,.5)
				text('x', 'Helvetica', 10, x[1],y[1]+15)
				tint(0,1,0,.5)
				text('y', 'Helvetica', 10, x[3]+15,y[3])
				tint(0,0,1,.5)
				text('z', 'Helvetica', 10, x[5]+15,y[5])
			stroke(0,0,0,.3)
			if mode==1:
				stroke(*o)
				for i in range(len(x)-1):
					if any(_[i]=='' for _ in (x,y,z)) or sum(_[i]**2 for _ in (x,y,z))**.5>300 or sum(_[i+1]**2 for _ in (x,y,z))**.5>300:
						continue
					line(x[i],y[i],x[i+1],y[i+1])
			if mode==2:
				l=len(x)
				for i in range(l-1):
					if any(_[i]=='' for _ in (x,y,z)) or sum(_[i]**2 for _ in (x,y,z))**.5>300:
						continue
					if (i+1)%o and x[i+1]!='' and sum(_[i+1]**2 for _ in (x,y,z))**.5<300:
						line(x[i],y[i],x[i+1],y[i+1])
					if i+o<l and x[i+o]!='' and sum(_[i+o]**2 for _ in (x,y,z))**.5<300:
						line(x[i],y[i],x[i+o],y[i+o])
			v=self.v
			s,c=math.sin,math.cos
			self.data[fn][1],self.data[fn][3]=[(i*c(v[0])-j*s(v[0])) if i!=''!=j else '' for i,j in zip(self.data[fn][1],self.data[fn][3])],[(-i*s(v[0])-j*c(v[0])) if i!=''!=j else '' for i,j in zip(self.data[fn][1],self.data[fn][3])]
			self.data[fn][3],self.data[fn][2]=[(j*s(v[1])-i*c(v[1])) if i!=''!=j else '' for i,j in zip(self.data[fn][3],self.data[fn][2])],[(i*s(v[1])+j*c(v[1])) if i!=''!=j else '' for i,j in zip(self.data[fn][3],self.data[fn][2])]
			fn+=1
		if len(self.touches):
			self.v=[19*i/20. for i in self.v]
		if len(self.touches)==2:
			t=self.touches.values()
			self.sc*=1+(distance(t[0].location,t[1].location)-distance(t[0].prev_location,t[1].prev_location))/200
			self.sc=max(self.sc,.001)
	
	def touch_began(self, touch):
		pass#self.v=[i/2. for i in self.v]
	
	def touch_moved(self, touch, d=False):	
		if len(self.touches)==1:
			self.v=[(self.v[i]+(j[0]-j[1])/150/(self.sc)**.5)/2 for i,j in enumerate(zip(touch.location,touch.prev_location))] if not d else [0,0]

	def touch_ended(self, touch):
		pass

a=Param()
run(a, frame_interval=2)
