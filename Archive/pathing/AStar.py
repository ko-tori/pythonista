from scene import *
from random import randint
from heapq import *
from console import hud_alert
import pickle

d=1
d2=2**.5

class AStar (Scene):
	def setup(self):
		self.w=85
		self.h=61
		self.sz=12
		self.grid=[[0 if randint(0,2) else 1 for i in range(self.w)] for i in range(self.h)]
		self.grid[31][43]=0
		self.loc=(self.w/2+1,self.h/2+1)
		self.dest=False
		self.path=False
		self.new=False
		self.dt2=0
	
	def draw(self):
		self.dt2+=self.dt
		w,h,s,g,loc,dest,path=self.w,self.h,self.sz,self.grid,self.loc,self.dest,self.path
		background(0, 0, 0)
		translate(4,4)
		fill(1,1,1)
		stroke(0,0,0)
		stroke_weight(.4)
		for y in range(h):
			for x in range(w):
				fill(*(1-g[y][x],)*3)
				rect(s*x,s*y,s,s)
		stroke(1,0,0)
		stroke_weight(1)
		if dest:
			line(s*dest[0]+1.5,s*dest[1]+1,s*dest[0]+s-1.5,s*dest[1]+11)
			line(s*dest[0]+1.5,s*dest[1]+11,s*dest[0]+10.5,s*dest[1]+1)
			if self.new:
				self.path=self.a()
				self.new=False
			elif path:
				for i in range(len(path)-1):
					line(path[i][0]*s+s/2,path[i][1]*s+s/2,path[i+1][0]*s+s/2,path[i+1][1]*s+s/2)
		fill(1,0,0)
		stroke_weight(0)
		ellipse(loc[0]*s+1,loc[1]*s+1,10,10)
		tint(0,1,0,.😎
		#text(str(self.dt2), 'Helvetica', 36, *self.bounds.center())
	
	def touch_began(self, touch):
		if self.dt2<.1:
			if len(self.touches)==4:
				with open('map', 'r') as f:
					self.grid=pickle.load(f)
					hud_alert('Loaded')
			if len(self.touches)==3:
				with open('map', 'w') as f:
					pickle.dump(self.grid, f)
					hud_alert('Saved')
			if len(self.touches)==2:
				self.grid=[[0 if randint(0,2) else 1 for i in range(self.w)] for i in range(self.h)]
				self.grid[31][43]=0
		self.dt2=0
	
	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch):
		if touch.location.x<self.w*self.sz and touch.location.y<self.h*self.sz:
			x,y=(int(i/self.sz) for i in touch.location)
			if self.grid[y][x]!=1:
				if self.path and self.dest==(x,y):
					self.loc=x,y
					self.dest=False
				else:
					self.dest=(x,y)
					self.new=True
		
	def a(self):
		open=[(self.heur(self.loc),0,self.loc)]
		closed=set()
		prev={}
		while len(open)>0:
			f,g,current=heappop(open)
			if current==self.dest:
				path=[current]
				while current in prev:
					current=prev[current]
					path.append(current)
				return path
			closed.add(current)
			for next in self.neighbors(current):
				if next in closed:
					continue
				g2=g+self.dist(current,next)
				if next not in (i[-1] for i in open):
					prev[next]=current
					heappush(open,(g2+self.heur(next),g2,next))
		return False				
	
	def neighbors(self, n):
		g=self.grid
		for x in -1,0,1:
			for y in -1,0,1:
				if x!=0 or y!=0:
					m=n[0]+x,n[1]+y
					if not(0<=m[0]<self.w and 0<=m[1]<self.h):
						continue
					if g[m[1]][m[0]]:
						continue
					if x and y and (g[n[1]][m[0]] or g[m[1]][n[0]]):
							continue
					yield m
			
	def dist(self, a, b):
		global d,d2
		if a[0]-b[0] and a[1]-b[1]:
			return d2
		return d
		
	def heur(self, n):
		dx = abs(n[0] - self.dest[0])
		dy = abs(n[1] - self.dest[1])
		return (d*(dx+dy)+(d2-2*d)*min(dx, dy))
		
test=AStar()
run(test)