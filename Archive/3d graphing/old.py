from scene import *
from math import *

axes=True
class Param(Scene):
	def setup(self):
		self.x=[-300,300,0,0,0,0]
		self.y=[0,0,-300,300,0,0]
		self.z=[0,0,0,0,-300,300]
		self.pts=[0,1,2,3,4,5] if axes else []
		self.v=[0,0,0]
		self.sc=15
		#self.graph(['sin(t)','cos(t)','t'])
		#self.graph(['sin(t)','cos(t)','t+pi'])
		#self.gparam()#['t**2','t*2','0'])
	
	def gparam(self, r=['sin(2*t)','sin(3*t)','cos(5*t)']):
		p=60/pi
		min=-pi
		max=pi
		t=min
		self.x.append(eval(r[0]))
		self.y.append(eval(r[1]))
		self.z.append(eval(r[2]))
		j=len(self.x)
		self.pts.append(j)
		for i in range(int(min*p),int(max*p)+1):
			t=(i+1)/p
			try:
				self.x.append(eval(r[0]))
				self.y.append(eval(r[1]))
				self.z.append(eval(r[2]))
				for _ in range(2):
					self.pts.append(j)
			except:
				self.x=self.x[:-1]
				self.y=self.y[:-1]
				self.z=self.z[:-1]
				self.pts=self.pts[:-2]
				j-=2
			j+=1
		#self.x=self.x[:-1]
		#self.y=self.y[:-1]
		#self.z=self.z[:-1]
		#self.pts=self.pts[:-1]
		
	def draw(self):
		background(*(1,)*3)
		translate(*self.bounds.center())
		background(1,1,1)
		x,y,z=([j for j in i] for i in (self.x,self.y,self.z))
		x[6:],y[6:],z[6:]=([i*self.sc for i in j] for j in (x[6:],y[6:],z[6:]))
		
		stroke_weight(2)
		stroke(1,0,0,.5)
		c=0 if axes else 3
		for i,j in zip(self.pts[::2],self.pts[1::2]):
			if c==1:
				stroke(0,1,0,.5)
			elif c==2:
				stroke(0,0,1,.5)
			elif c>2:
				stroke(0,0,0,.3)
			line(x[i],y[i],x[j],y[j])
			c+=1
		if axes:
			tint(1,0,0,.5)
			text('x', 'Helvetica', 10, x[1],y[1]+15)
			tint(0,1,0,.5)
			text('y', 'Helvetica', 10, x[3]+15,y[3])
			tint(0,0,1,.5)
			text('z', 'Helvetica', 10, x[5]+15,y[5])
		s,c=math.sin,math.cos
		self.x,self.z=[i*c(self.v[0])-j*s(self.v[0]) for i,j in zip(self.x,self.z)],[-i*s(self.v[0])-j*c(self.v[0]) for i,j in zip(self.x,self.z)]
		self.z,self.y=[j*s(self.v[1])-i*c(self.v[1]) for i,j in zip(self.z,self.y)],[i*s(self.v[1])+j*c(self.v[1]) for i,j in zip(self.z,self.y)]
		if len(self.touches):
			self.v=[9*i/10. for i in self.v]
		if len(self.touches)==2:
			t=self.touches.values()
			self.sc*=1+(t[0].location.distance(t[1].location)-t[0].prev_location.distance(t[1].prev_location))/200
			self.sc=max(self.sc,.001)
	
	def touch_began(self, touch):
		pass#self.v=[i/2. for i in self.v]
	
	def touch_moved(self, touch, d=False):	
		if len(self.touches)==1:
			self.v=[(self.v[i]+(j[0]-j[1])/150/(self.sc)**.5)/2 for i,j in enumerate(zip(touch.location,touch.prev_location))] if not d else [0,0]

	def touch_ended(self, touch):
		pass

a=Param()
run(a)
