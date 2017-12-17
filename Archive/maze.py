from scene import *
from collections import deque
from random import randint

def wall():
	p=[64, 12, 4, 8]
	a=['1000','0100','0010','0001','1100','0110','0011','1001','1010','0101','0000']
	r=randint(0,sum(p))
	c='0000'
	#single walls
	if p[0]>3 and 0<=r<p[0]:
		c=a[r/(p[0]/4)]
	#corners
	if p[1]>3 and p[0]<=r<p[0]+p[1]:
		c=a[(r-p[0])/(p[1]/4)+4]
	#parallels
	if p[2]>1 and p[0]+p[1]<=r<p[0]+p[1]+p[2]:
		c=a[(r-(p[0]+p[1]))/(p[2]/2)+8]
	#empty
	if p[3]>0 and p[0]+p[1]+p[2]<=r<=sum(p):
		c=a[10]
	return c

def generate(w,h):
	g=[[0 for _ in range(w)] for _ in range(h)]
	for i in range(h):
		for j in range(w):
			g[i][j]=wall()
	return deque([deque(i) for i in g])

class MyScene (Scene):
	def setup(self):
		self.cells=generate(int(self.bounds.w/31)+3, int(self.bounds.h/31)+3)
		self.x=5
		self.y=-10
		self.m=False
	
	def draw(self):
		stroke_weight(1)
		stroke(0,0,0)
		background(1,1,1)
		tint(0,0,0)
		fill(1,0,0)
		
		push_matrix()
		translate(*self.bounds.center())
		rect(0, 0, 7, 7)
		pop_matrix()
		
		#scale 0.5x
		#push_matrix();scale(0.5);translate(self.bounds.w/2, self.bounds.h/2)
		clst=[]
		stroke(0,0,0)
		for y,i in enumerate(self.cells):
			for x,j in enumerate(i):
				if abs(x-(int(self.bounds.w/31)+1)/2+self.x/31.)<1.5 and abs(y-(int(self.bounds.h/31)+2)/2+self.y/31.)<1.5:
					#stroke(1,0,0)
					clst.append((j,x,y))
				a,b=31*x+self.x-31,31*y+self.y-30
				if j[0]=='1':
					#stroke(1,0,0)
					line(a,b,a+31,b)
					#stroke(0,0,0)
				if j[1]=='1':
					line(a+31,b,a+31,b+31)
				if j[2]=='1':
					line(a,b+31,a+31,b+31)
				if j[3]=='1':
					line(a,b,a,b+31)
				stroke(0,0,0)
		
		#pop_matrix()
		
		dx=0
		dy=0	
		if len(self.touches.values())==1 and self.m:
			touch=self.touches.values()[0].location
			dx=(self.m[0]-touch.x)/100.
			if dx>2:
				dx=2
			dy=(self.m[1]-touch.y)/100.
			if dy>2:
				dy=2
			
			push_matrix()
			translate(0,0)
			stroke(1,0,0)
			line(self.m[0], self.m[1], *touch)
			pop_matrix()
			
		stroke(0,1,0)
		for j,x,y in clst:
			pass
			
		for j,x,y in clst:
			a,b=31*x+self.x-31,31*y+self.y-30
			rx,ry=self.bounds.center()
			ellipse(a,b,2,2)
			ellipse(rx,ry,2,2)
			if j[0]=='1':
				if (abs(b-ry-7)<abs(dy)+1 or abs(b-ry)<abs(dy)+1) and dy>0 and a<=rx<=a+31:
					dy=0
			if j[1]=='1':
				pass#line(a+31,b,a+31,b+31)
			if j[2]=='1':
				if (abs(b-ry-31)<abs(dy)+1 or abs(b-ry-7)<abs(dy)+1) and dy<0 and a<=rx<=a+31:
					dy=0
			if j[3]=='1':
				pass#line(a,b,a,b+31)
		
		self.x+=dx
		self.y+=dy
		
		if self.x>31:
			self.x-=31
			self.wadd()
		if self.x<-31:
			self.x+=31
			self.eadd()
		if self.y>31:
			self.y-=31
			self.nadd()
		if self.y<-31:
			self.y+=31
			self.sadd()
		
	def touch_began(self, touch):
		if not self.m:
			self.m=touch.location.as_tuple()
	
	def touch_ended(self, touch):
		self.m=False
		
	def eadd(self):
		for row in self.cells:
			row.popleft()
			row.append(wall())
		
	def wadd(self):
		for row in self.cells:
			row.pop()
			row.appendleft(wall())
		
	def nadd(self):
		self.cells.appendleft(deque([wall() for i in range(len(self.cells[0]))]))
		self.cells.pop()
		
	def sadd(self):
		self.cells.append(deque([wall() for i in range(len(self.cells[0]))]))
		self.cells.popleft()

scene=MyScene()
run(scene)
