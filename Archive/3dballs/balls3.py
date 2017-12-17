# coding: utf-8

from scene import *
import sound
import random
import math
import ui
import colorsys
A = Action

boxdim=768.,576.,512.

def dot(u,v):
	return sum(i*j for (i,j) in zip(u,v))

class Rect3 (object):
	def __init__(self, x, y, z, w=128.,h=96.,d=64.,v=1, makenode=True):
		self.pos=tuple(float(i) for i in (x,y,z))
		self.dim=(w,h,d)
		self.v=v
		if makenode:
			self.node=self.makenode()
		
	def makenode(self):
		u=ui.Path()
		u.line_width=1
		dz=boxdim[2]
		for (x1,y1,z1),(x2,y2,z2) in list(self.iteredges())[:]:
			#x1-=384
			#x2-=384
			y1=-y1
			y2=-y2
			#y1-=288
			#y2-=288
			u.move_to(x1*dz/(dz+z1),y1*dz/(dz+z1))
			u.line_to(x2*dz/(dz+z2),y2*dz/(dz+z2))
			#print x2*dz/(dz+z2),y2*dz/(dz+z2)
			#print x1*dz/(2*dz+z1)+512,y1*dz/(2*dz+z1)+384
		#print x1,y1
		u=ShapeNode(u,position=((x1-128)*dz/(dz+z1)+512, 128+y1*dz/(dz+z1)))
		u.anchor_point=(0,0)
		u.stroke_color=(1,0,0)
		return u
		
	def iteredges(self):
		x,y,z=self.pos
		w,h,d=self.dim
		yield (x,y,z),(x+w,y,z)
		yield (x,y,z),(x,y+h,z)
		yield (x,y,z),(x,y,z+d)
		yield (x+w,y,z),(x+w,y+h,z)
		yield (x+w,y,z),(x+w,y,z+d)
		yield (x,y+h,z),(x+w,y+h,z)
		yield (x,y+h,z),(x,y+h,z+d)
		yield (x,y,z+d),(x+w,y,z+d)
		yield (x,y,z+d),(x,y+h,z+d)
		yield (x,y+h,z+d),(x+w,y+h,z+d)
		yield (x+w,y,z+d),(x+w,y+h,z+d)
		yield (x+w,y+h,z),(x+w,y+h,z+d)
		
	def __contains__(self, p, r=None):
		if not r:
			if isinstance(p, Ball):
				r=p.r
			else:
				r=0
		x,y,z=p
		x0,y0,z0=self.pos
		w,h,d=self.dim
		r=p.r
		for cx in (x0,x0+w):
			for cy in (y0,y0+h):
				for cz in (z0,z0+d):
					if (cx-x)**2+(cy-y)**2+(cz-z)**2<=r**2:
						return True
		if x0-r<=x<=x0+w+r and y0-r<=y<=y0+h+r and z0-r<=z<=z0+d+r:
			if not x0<=x<=x0+w or not y0<=y<=y0+h or not z0<=z<=z0+d:
				return False
			return True
		return False
		
	def collide(self,ball):
		#x,y,z=ball
		r=ball.r
		#x0,y0,z0=self.pos
		#w,h,d=self.dim
		for n,(i,j,k) in enumerate(zip(self.pos,ball,self.dim)):
			if i-r<=j:
				ball.v[n]*=-1
				ball.pos[n]=2*i-2*r-j
			elif j<=i+k+r:
				ball.v[n]*=-1
				ball.pos[n]=2*(i+k+r)-j
				
	def __repr__(self):
		return str(self.pos)

class Ball (object):
	def __init__(self,x,y,z):
		self.pos=[x,y,z]
		self.r=20.
		self.v=[0,0,3]
		self.v=[random.randint(-15,15),random.randint(-15,15),random.randint(1,15)]
		self.node=Node(position=(512,384))
		#self.node=SpriteNode(position=(512,384),color=(1,0,0),alpha=.5)
		self.node.size=boxdim[:2]
		p=ui.Path.oval(0,0,2*self.r,2*self.r)
		self.sprite=ShapeNode(p,position=self.pos)
		self.sprite.fill_color=colorsys.hsv_to_rgb(random.random(),1,1)+(.8,)
		self.node.add_child(self.sprite)
		
	def __iter__(self):
		for i in self.pos:
			yield i
			
	def move(self):
		for i in (0,1,2):
			self.pos[i]+=self.v[i]
		x,y,z=self.pos
		dx,dy,dz=(i/2 for i in boxdim)
		r=self.r
		vi=[i for i in self.v]
		if x<r-dx:
			self.v[0]*=-1
			self.pos[0]=-2*dx+2*r-x
		if x>dx-r:
			self.v[0]*=-1
			self.pos[0]=2*dx-2*r-x
		if y<r-dy:
			self.v[1]*=-1
			self.pos[1]=-2*dy+2*r-y
		if y>dy-r:
			self.v[1]*=-1
			self.pos[1]=2*dy-2*r-y
		if z<r:
			self.v[2]*=-1
			self.pos[2]=2*r-z
		if z>2*dz-r:
			self.v[2]*=-1
			self.pos[2]=4*dz-z-2*r
			print 'back'+str(random.random())
		if vi!=self.v:
			sound.play_effect('sound/drop.mp3',.5,1-self.pos[2]/1024)
		self.sprite.position=self.pos[:2]
		self.node.z_position=-self.pos[2]
		self.node.scale=2*dz/(2*dz+self.pos[2])

class Game (Scene):
	def setup(self):
		self.background_color=(1,1,1)
		dx,dy,dz=(i/2 for i in boxdim)
		dz*=2
		self.box=Rect3(-dx,-dy,0,dx*2,dy*2,dz,makenode=False)
		u=ui.Path()
		u.line_width=1
		for (x1,y1,z1),(x2,y2,z2) in self.box.iteredges():
			u.move_to(x1*dz/(dz+z1),y1*dz/(dz+z1))
			u.line_to(x2*dz/(dz+z2),y2*dz/(dz+z2))
			#print x1*dz/(2*dz+z1)+512,y1*dz/(2*dz+z1)+384
		u=ShapeNode(u,position=(x1*dz/(dz+z1)-256,y1*dz/(dz+z1)-192),z_position=-10**10)
		u.anchor_point=(0,0)
		u.stroke_color=(.6,)*3
		self.add_child(u)
		self.balls=[]
		self.blocks=[]
		self.addblock((-3,-3))
		for x in range(6):
			for y in range(6):
				if random.random()<.7: continue
				#self.addblock((x-3,y-3))
		self.test=LabelNode(position=self.bounds.center())
		self.test.color=(0,0,0)
		self.add_child(self.test)
	
	def did_change_size(self):
		pass
	
	def update(self):
		if self.balls:
			self.test.text=str(self.balls[0].pos)
		for i in self.balls:
			i.move()
			for j in self.blocks:
				if i in j:
					j.collide(i)
	
	def touch_began(self, touch):
		x,y=touch.location
		self.addball(x-512,y-384)
	
	def touch_moved(self, touch):
		pass
	
	def touch_ended(self, touch):
		pass
		
	def addball(self,x,y):
		b=Ball(x,y,20)
		self.balls.append(b)
		self.add_child(b.node)
		
	def addblock(self,pos=None):
		if pos is None:
			x=random.randint(-3,3)
			y=random.randint(-3,3)
			x=y=0
		else:
			x,y=pos
		z=448.
		r=Rect3(128*x,96*y,z)
		self.add_child(r.node)
		self.blocks.append(r)

s=Game()
run(s, orientation=LANDSCAPE,show_fps=False)