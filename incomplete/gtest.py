from scene import *
from itertools import combinations
from random import randint
from vec import *

crw=0.8

class Ball:
	def __init__(self, p, v, r, m, cr=0.8, c=(1,0,0,0.5)):
		self.p=p
		self.v=v
		self.r=r
		self.m=m
		self.c=c
		self.cr=cr
		
	def addv(self, dt):
		return Ball(self.p+self.v*dt, self.v, self.r, self.m, self.c)
		
	def back(self, dt):
		self.p-=self.v*dt
		
	def move(self, dt):
		self.p+=self.v*dt

class MyScene (Scene):
	def setup(self):
		#a=Ball(Vec2(412, 418), Vec2(randint(-10,10), randint(-10,10)), 10, 10, 0.8, (0,0,1,0.5))
		#b=Ball(Vec2(612, 318), Vec2(randint(-10,10), randint(-10,10)), 50, 500000, 0.8, (1,0,0,0.5))
		#c=Ball(Vec2(512, 418), Vec2(randint(-10,10), randint(-10,10)), 10, 10, 0.8, (1,1,0,0.5))
		#d=Ball(Vec2(712, 418), Vec2(randint(-10,10), randint(-10,10)), 10, 10, 0.8, (0,1,0,0.5))
		#e=Ball(Vec2(512, 618), Vec2(randint(-10,10), randint(-10,10)), 10, 10, 0.8, (0,1,1,0.5))
		self.o=[]#[a,b,c,d,e]
		self.mode=0
	
	def draw(self):
		background(1,1,1)
		
		for i,j in combinations(self.o, 2):
			d=Vec2(i.p.x-j.p.x,i.p.y-j.p.y)
			if abs(d) <= i.r + j.r:
				i.p=j.p+d.unit()*(i.r+j.r)
				j.p=i.p-d.unit()*(i.r+j.r)
				d=d.perp()
				#r=i.m/j.m
				i.v=i.cr*j.cr*i.v.reflect(d)#*(j.m/i.m)
				j.v=i.cr*j.cr*j.v.reflect(d)#*(i.m/j.m)
				i.move(self.dt)
				j.move(self.dt)
		
		for i in self.o:
			fill(*i.c)
			ellipse(i.p.x - i.r, i.p.y - i.r, 2*i.r, 2*i.r)
			j=i.addv(self.dt)
			if not i.r<j.p.x<self.bounds.w-i.r:
				if i.r<j.p.x: i.p.x=self.bounds.w-i.r
				else: i.p.x=i.r
				i.v.x*=-crw
			if not i.r<j.p.y<self.bounds.h-i.r:
				if i.r<j.p.y: i.p.y=self.bounds.h-i.r
				else: i.p.y=i.r
				i.v.y*=-crw
			g=gravity()
			#g=(0,0,0)
			i.v.x+=g[0]/self.dt
			i.v.y+=g[1]/self.dt
			#text(str(g), 'Helvetica', 12, *self.bounds.center())	
			i.move(self.dt)
			
		#text(str(i.vy), 'Helvetica', 36, *i.bounds.center())
	
	def touch_began(self, touch):
		pass
	
	def touch_moved(self, touch):
		self.mode=1
		self.o=[i for i in self.o if not touch.location in Rect(i.p.x-i.r,i.p.y-i.r,2*i.r,2*i.r)]

	def touch_ended(self, touch):
		if self.mode==0:
			self.o.append(Ball(Vec2(*touch.location), Vec2(randint(-10,10), randint(-10,10)), 100, 10, 0.8, (randint(5,8)/10.,randint(5,8)/10.,randint(2,8)/10.,0.5)))
		if len(self.touches)==0:
			self.mode=0

test=MyScene()
run(test)
