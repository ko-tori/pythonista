from scene import *
from random import *

p=.5+5**.5/2

TETRA=[[1,-1,1,-1]
		  ,[-1,1,1,-1]
		  ,[1,1,-1,-1]
		  ,[0,1,0,2,0,3,1,2,2,3,3,1],
		  1.4]
CUBE=[[1,1,-1,-1,1,1,-1,-1]
		 ,[1,-1,-1,1,1,-1,-1,1]
		 ,[1,1,1,1,-1,-1,-1,-1]
		 ,[0,1,1,2,2,3,3,0,0,4,1,5,2,6,3,7,4,5,5,6,6,7,7,4],
		 1.5]
OCTA=[[2,0,0,-2,0,0]
		 ,[0,2,0,0,-2,0]
		 ,[0,0,2,0,0,-2]
		 ,[0,2,1,2,3,2,4,2,0,1,1,3,3,4,4,0,0,5,1,5,3,5,4,5]]
DODECA=[[1,1/p,1,p,p,0,-1/p,0,1,1,-1,-1,0,1/p,0,-1,-p,-p,-1,-1/p]
			 ,[1,0,-1,-1/p,1/p,p,0,-p,-1,1,1,-1,-p,0,p,1,1/p,-1/p,-1,0]
			 ,[1,p,1,0,0,1/p,p,1/p,-1,-1,1,1,-1/p,-p,-1/p,-1,0,0,-1,-p]
			 ,[0,1,1,2,2,3,3,4,4,0,0,5,1,6,2,7,3,8,4,9,5,10,10
			  ,6,6,11,11,7,7,12,12,8,8,13,13,9,9,14,14,5,10,16
			  ,11,17,12,18,13,19,14,15,15,16,16,17,17,18,18,19,19,15]
			 ,1.5]
ICOSA=[[0,p,1,0,p,-1,0,-p,1,0,-p,-1],[1,0,p,-1,0,p,1,0,-p,-1,0,-p],[p,1,0,p,-1,0,-p,1,0,-p,-1,0]
      ,[0,1,1,3,3,0,0,2,2,1,1,8,8,3,3,7,7,0,0,5,1,4,3,11,5,2,2,4,4,8,8,11,11,7,7,5
       ,7,10,10,5,5,6,6,2,6,4,4,9,9,8,9,11,11,10,6,9,9,10,10,6],
       1.3]
RDODECA=[[
          
          ]]

SHAPES=[TETRA,CUBE,OCTA,DODECA,ICOSA]

class Three (Scene):
	def __init__(self, shape):
		self.shape=shape
		
	def setup(self):
		try:
			s=self.shape[4]
		except:
			s=1
		self.x,self.y,self.z=[[s*i for i in j] for j in self.shape[:3]]
		self.pts=self.shape[3]
		self.v=[0,0,0]
		self.touch_moved(None,1)
		self.re=0
	
	def draw(self):
		if len(self.touches)==3:
			self.re=1
		translate(*self.bounds.center())
		background(1,1,1)
		x,y,z=[[j for j in i] for i in (self.x,self.y,self.z)]
		if self.shape!=TETRA:
			for i in range(len(self.x)):
				x[i]*=5/(z[i]+6)
				y[i]*=5/(z[i]+6)
		x,y,z=([150*i for i in j] for j in (x,y,z))
		stroke_weight(2)
		stroke(1,0,0,.5)
		for i,j in zip(self.pts[::2],self.pts[1::2]):	
			line(x[i],y[i],x[j],y[j])
		s,c=math.sin,math.cos
		self.x,self.z=[i*c(self.v[0])-j*s(self.v[0]) for i,j in zip(self.x,self.z)],[-i*s(self.v[0])-j*c(self.v[0]) for i,j in zip(self.x,self.z)]
		self.z,self.y=[j*s(self.v[1])-i*c(self.v[1]) for i,j in zip(self.z,self.y)],[i*s(self.v[1])+j*c(self.v[1]) for i,j in zip(self.z,self.y)]
		if len(self.touches):
			self.v=[9*i/10. for i in self.v]
	
	def touch_began(self, touch):
		pass#self.v=[i/2. for i in self.v]
	
	def touch_moved(self, touch, d=False):	
		self.v=[(self.v[i]+(j[0]-j[1])/200)/2 for i,j in enumerate(zip(touch.location,touch.prev_location))] if not d else [0,0]

	def touch_ended(self, touch):
		if self.re and len(self.touches)==0:
			a=Three(choice(SHAPES))
			run(a)

test=Three(choice(SHAPES))
run(test)