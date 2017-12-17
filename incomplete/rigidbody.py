from scene import *
from glib import *
import numpy as np

def unit_vector(v):
	return v / np.linalg.norm(v)

def angle_between(v1, v2):
	return np.arccos(np.clip(np.dot(unit_vector(v1), unit_vector(v2)),-1,1))
	
def dot(a,b):
	return a[0] * b[0] + a[1] * b[1]
	
def cross(a,b):
	return a[0] * b[1] - a[1] * b[0]

class Poly:
	def __init__(self, d, x, y, m, v=[0,0], va=0):
		if len(x) != len(y):
			raise TypeError('bad')
		self.n=len(x)
		self.x=x
		self.y=y
		self.d=d
		self.a=0
		self.va=va
		self.m=m
		self.v=v
		temp=zip(x,y)
		self.i=m/6.*sum([abs(cross(temp[i],temp[i+1]))*(dot(temp[i], temp[i])+dot(temp[i],temp[i+1])+dot(temp[i+1],temp[i+1])) for i in range(-1,self.n-1)])/sum([abs(cross(temp[i],temp[i+1])) for i in range(-1,self.n-1)])
		
	def __contains__(self, item):
		n=len(self.x)
		x=self.x
		y=self.y
		x2, y2=item[0]+self.d[0], item[1]+self.d[1]
		j = n-1
		c = False
		for i in range(n):
			if ((y[i]>y2) != (y[j]>y2)) and (x2 < (x[j]-x[i]) * (y2-y[i]) / (y[j]-y[i]) + x[i]):
				c = not c
			i += 1
			j = i-1
		return c

	def v(self):
		return np.linalg.norm(v)
		
	def __len__(self):
		return len(self.x)
	
	def __iter__(self):
		for i in zip(self.x, self.y):
			yield i
			
	def draw(self):
		poly(self.d[0], self.d[1], self.x, self.y, self.a)
		
	def update(self, dt):
		self.d[0]=self.d[0]+self.v[0]*dt
		self.d[1]=self.d[1]+self.v[1]*dt
		self.a=self.a+self.va*dt
		
	def accel(self, x=0, y=0, a=0):
		self.v[0]+=x
		self.v[1]+=y
		self.va+=a
		
	def force(self, x, y, a, b):
		self.v[0]+=x/self.m
		self.v[1]+=y/self.m
		self.va+=(x*b - y*a)/self.i
		
	def moment(self):
		return self.m
	
	def collide(self):
		pass

class Physics (Scene):
	def setup(self):
		self.objects=[]
		o=Poly([512, 318], [-10,10,10,-20], [-10,-10,10,10], 10, [1, 10], 10)
		self.objects.append(o)

	def draw(self):
		background(0,0,0)
		w,h=self.bounds.w, self.bounds.h
		ag=[5*i for i in gravity().as_tuple()[0:2]]
		for obj in self.objects:
			for pt in obj:
				proj=(pt[0]+obj.v[0],pt[1]+obj.v[1])
				#if 
			stroke_weight(1)
			obj.draw()
			obj.update(self.dt)
			#obj.accel(y=-9.8)
			obj.accel(*ag)
			for x,y in zip(obj.x,obj.y):
				if x>w-1:
					vec=(-1,0)
				if x<1:
					vec=(1,0)
				if y>h-1:
					vec=(0,-1)
				if y<1:
					vec=(0,1)
				obj.collide(x,y,ag[0],ag[1])

	def touch_began(self, touch):
		pass

	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch):
		pass

test=Physics()
run(test)
#print 'start'
#for i in range(100000): 
temp = Poly([512, 318], [-10,10,10,-20], [-10,-10,10,10], 10, [1, 10], 10)
#print 'done'

