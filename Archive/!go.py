from scene import *
from glib import roundrect

test=0

class Game (Scene):
	def setup(self):
		#settings
		self.players=2
		self.w=19
		self.h=19
		self.zoom=.75
		self.number=False
		self.showHitbox=False
		self.showLast=False#(1,0,0)
		self.suicides=True
		
		self.std19=0#set true to make standard board
		if self.std19:
			self.w=19
			self.h=19
			self.zoom=.75
		
		self.dx=self.bounds.w/2
		self.dy=self.bounds.h/2
		self.grid=[[0 for _ in range(self.w)] for _ in range(self.h)]
		self.loc=False
		self.mode=0
		self.col=1
		self.won=0
		self.past=False
		self.undo=Rect(120,10,100,50)
		self.reset=Rect(10,10,100,50)
		self.passb=Rect(230,10,100,50)
		self.passn=0
		self.temp=0
		self.msgc=(.5)*3
		self.msgt=0
	
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
						p=[(j,i)]
						p.append(self.check(i-1,j))
						p.append(self.check(i,j-1))
						p.append(self.check(i+1,j))
						p.append(self.check(i,j+1))
						if self.past:
							self.past.append(p)
						else:
							self.past=[p]
						self.col=1 if self.col>=self.players else self.col+1
						self.passn=0
						self.loc=False
						if (not self.suicides and not self.alive(i,j,[])) or (len(self.past)>1 and any(len(a)==2 and (i,j)==a[1] for a in self.past[-2][1:])):
							self.msg='Invalid Move'
							self.msgc=(1,0,0)
							self.msgt=1
							self.undof()
							self.grid[j][i]=0
						if self.suicides and self.check(i,j):
							self.msg='Suicided'
							self.msgc=(1,0,0)
							self.msgt=1
				stroke(*b+(.7,))
				if self.grid[j][i]>0:
					stroke_weight(0)
					fill(*((self.grid[j][i]-1.)/(self.players-1),)*3)#+(.9,))
					if self.showLast and self.past[-1][0]==(j,i):
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
		if self.won:
			fill(.42,.38,.3)
			tint(*(.5,)*3)
		roundrect(*self.passb.as_tuple())
		text('Pass', 'Helvetica', 20, *self.passb.center().as_tuple())
		fill(*b)
		tint(*w)
		if not self.past and not self.passn:
			fill(.42,.38,.3)
			tint(*(.5,)*3)
		roundrect(*self.undo.as_tuple())
		text('Undo', 'Helvetica', 20, *self.undo.center().as_tuple())
		#fill(*b)
		if self.won==-1:
			tint(*(.5,)*3)
			#tint(*((self.won-1.)/(self.players-1),)*3)
			text('Game Over', 'Helvetica', 72, *self.bounds.center())
		tint(*(.5,)*3)
		if self.msgt:
			self.msgt-=.02
			tint(*self.msgc+(self.msgt,))
			text(self.msg, 'Helvetica', 30, *self.bounds.center())
	
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
			elif touch.location in self.undo and (self.passn or self.past):
				self.undof()
			elif self.won:
				return
			elif touch.location in self.passb:
				self.col=1 if self.col>=self.players else self.col+1
				self.passn+=1
				if self.passn>=self.players:
					self.won=-1
			elif not self.won:
				self.temp=self.loc=Point((touch.location.x-self.dx)/self.zoom+25*self.w,(touch.location.y-self.dy)/self.zoom+25*self.h)
				
	def undof(self):
		if self.passn:
			self.passn-=1
		elif self.past:
			self.grid[self.past[-1][0][0]][self.past[-1][0][1]]=0
			for i0 in self.past[-1][1:]:
				if len(i0)==0:
					continue	
				n1=i0[0]
				for i1,j1 in i0[1:]:
					self.grid[j1][i1]=n1
			self.past=self.past[:-1]
		self.won=0
		#self.check(*reversed(self.past[-1][0]))
		self.col=self.players if self.col<=1 else self.col-1
				
	def should_rotate(self, o):
		return True

	def alive(self, i, j, group):
		if (i,j) in group:
			return False
		group.append((i,j))
		g,h,w=self.grid,self.h,self.w
		n=g[j][i]
		return (j>0 and (self.alive(i,j-1, group) if g[j-1][i]==n else g[j-1][i]==0)) or (i>0 and (self.alive(i-1,j,group) if g[j][i-1]==n else g[j][i-1]==0)) or (j<h-1 and (self.alive(i,j+1,group) if g[j+1][i]==n else g[j+1][i]==0)) or (i<w-1 and (self.alive(i+1,j,group) if g[j][i+1]==n else g[j][i+1]==0))

	def check(self,i,j):
		g,h,w=self.grid,self.h,self.w
		if i<0 or j<0 or i>=h or j>=w:
			return []
		n=g[j][i]
		if n==0:
			return []
		group=[]
		if not self.alive(i,j,group):
			for a,b in group:
				self.grid[b][a]=0
			return [n]+group
		return []

test=Game()
run(test, orientation=LANDSCAPE)