from scene import *
from glib import roundrect

test=0

class Game (Scene):
	def setup(self):
		#settings
		self.players=2
		self.xinarow=5
		self.w=19
		self.h=19
		self.zoom=.75
		self.number=False
		self.showHitbox=False
		self.showLast=(1,0,0)
		
		self.std19=False#set true to make standard board
		if self.std19:
			self.w=19
			self.h=19
			self.zoom=.75
		
		self.dx=self.bounds.w/2
		self.dy=self.bounds.h/2
		self.grid=[[0 for _ in range(self.w)] for _ in range(self.h)]
		self.loc=False
		self.mode=0
		self.col=self.players+1
		self.won=0
		self.past=False
		self.undo=Rect(120,10,100,50)
		self.reset=Rect(10,10,100,50)
		self.temp=0
	
	def draw(self):
		b=.6,.4,0
		w=(1,)*3
		background(*((self.col-1.)/(self.players-1),)*3)
		push_matrix()
		translate(self.dx, self.dy)
		scale(self.zoom)
		translate(-25*self.w,-25*self.h)
		stroke(0,0,0)
		stroke_weight(1)
		fill(*b+(.7,))
		rect(0,0,50*self.w+10,50*self.h+10)
		stroke_weight(0.5/self.zoom)
		fill(*b+(0,))
		rect(25,25,50*self.w-40,50*self.h-40)
		for i in range(self.w-1):
			for j in range(self.h-1):
				rect(50*i+30,50*j+30,50,50)
		if self.std19:
			stroke_weight(1/self.zoom)
			fill(*(0,)*3)
			ellipse(180-6,180-6,12,12)
		stroke(0,0,0)
		stroke_weight(0)
		cell=False
		for i in range(self.w):
			for j in range(self.h):
				r=Rect(50*i+5,50*j+5,50,50)
				if self.showHitbox:
					stroke_weight(1)
					stroke(1,0,0)
					fill(0,0,0,0)
					rect(*r.as_tuple())
				if self.mode==0 and self.loc:
					if not self.won and not cell and self.loc in r and self.grid[j][i]==0:
						cell=True
						self.grid[j][i]=self.col
						if self.past:
							self.past.append((j,i))
						else:
							self.past=[(j,i)]
						self.check(i,j)
						self.col=1 if self.col>=self.players else self.col+1
						self.loc=False
				stroke(*b+(.7,))
				if self.grid[j][i]>0:
					stroke_weight(0)
					fill(*((self.grid[j][i]-1.)/(self.players-1),)*3)#+(.9,))
					if self.showLast and self.past[-1]==(j,i):
						stroke_weight(1/self.zoom)
						stroke(*self.showLast)
					ellipse(50*i+15,50*j+15,30,30)
					if self.number:
						tint(*(-int((self.grid[j][i]-1.)/(self.players-1)+.5)+1,)*3)
						text(str(self.grid[j][i]), 'Helvetica', 36/(len(str(self.grid[j][i]))+1)**.7, 50*i+30, 50*j+30)					
		pop_matrix()
		fill(*b)
		tint(*w)
		roundrect(*self.reset.as_tuple())
		text('Reset', 'Helvetica', 20, *self.reset.center().as_tuple())
		if not self.past:
			fill(.42,.38,.3)
			tint(*(.5,)*3)
		roundrect(*self.undo.as_tuple())
		text('Undo', 'Helvetica', 20, *self.undo.center().as_tuple())
		#fill(*b)
		if self.won>0:
			tint(*((self.won-1.)/(self.players-1),)*3)
			text('GG', 'Helvetica', 72, *self.bounds.center())
		elif self.won==-1:
			tint(*(.5,)*3)
			text('Draw?!', 'Helvetica', 72, *self.bounds.center())
		#tint(*(.5,)*3)
		#text(str(self.temp), 'Helvetica', 36, *self.bounds.center())
	
	def touch_began(self, touch):
		self.mode=2
	
	def touch_moved(self, touch):
		self.mode=1
		self.dx+=touch.location.x-touch.prev_location.x
		self.dy+=touch.location.y-touch.prev_location.y

	def touch_ended(self, touch):
		if len(self.touches)==0 and self.mode!=1:
			self.mode=0
			if touch.location in self.reset:
				global test
				run(test,orientation=LANDSCAPE)
			elif self.past and touch.location in self.undo:
				self.grid[self.past[-1][0]][self.past[-1][1]]=0
				self.won=0
				self.check(*reversed(self.past[-1]))
				self.past=self.past[:-1]
				self.col=self.players if self.col<=1 else self.col-1
			elif not self.won:
				self.temp=self.loc=Point((touch.location.x-self.dx)/self.zoom+25*self.w,(touch.location.y-self.dy)/self.zoom+25*self.h)
				
	def should_rotate(self, o):
		return True

	def check(self,i,j):
		g=self.grid
		h=self.h
		w=self.w
		n=g[j][i]
		x=[[0,1] for _ in range(8)]
		for k in range(1,self.h):
			if x[0][1] and j-k>=0 and i-k>=0 and g[j-k][i-k]==n: x[0][0]+=1
			else: x[0][1]=0
			if x[4][1] and j+k<h and i+k<w and g[j+k][i+k]==n: x[4][0]+=1
			else: x[4][1]=0
			if x[1][1] and j-k>=0 and g[j-k][i]==n: x[1][0]+=1
			else: x[1][1]=0
			if x[5][1] and j+k<h and g[j+k][i]==n: x[5][0]+=1
			else: x[5][1]=0
			if x[2][1] and j-k>=0 and i+k<w and g[j-k][i+k]==n: x[2][0]+=1
			else: x[2][1]=0
			if x[6][1] and j+k<h and i-k>0 and g[j+k][i-k]==n: x[6][0]+=1
			else: x[6][1]=0
			if x[3][1] and i-k>=0 and g[j][i-k]==n: x[3][0]+=1
			else: x[3][1]=0
			if x[7][1] and i+k<w and g[j][i+k]==n: x[7][0]+=1
			else: x[7][1]=0
			if not any(lol[1] for lol in x): break
		x=[_[0] for _ in x]
		x=[sum(_)+1 for _ in zip(x[:4],x[4:])]
		if self.xinarow in x:
			self.won=n
		elif all(all(_) for _ in g):
			self.won=-1

test=Game()
run(test, orientation=LANDSCAPE)