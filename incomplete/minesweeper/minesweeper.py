from scene import *
from random import randint
import Image

t_ct=0
t_type=0 #0:still, 1:moving
t_loc=False
first=True

def number(grid):
	for y in range(len(grid)):
		for x in range(len(grid[0])):
			grid[y][x][0]=-1 if grid[y][x][0]==-1 else 0
			if grid[y][x]!=-1:
				if y>0 and grid[y-1][x][0]==-1:grid[y][x][0]+=1
				if y<len(grid)-1 and grid[y+1][x][0]==-1:grid[y][x][0]+=1
				if x>0:
					if y>0 and grid[y-1][x-1][0]==-1:grid[y][x][0]+=1
					if grid[y][x-1][0]==-1:grid[y][x][0]+=1
					if y<len(grid)-1 and grid[y+1][x-1][0]==-1:grid[y][x][0]+=1
				if x<len(grid[y])-1:
					if y>0 and grid[y-1][x+1][0]==-1:grid[y][x][0]+=1
					if grid[y][x+1][0]==-1:grid[y][x][0]+=1
					if y<len(grid)-1 and grid[y+1][x+1][0]==-1:grid[y][x][0]+=1

class Game (Scene):
	def setup(self):
		self.scale=1.5
		self.dx=0
		self.dy=0
		self.grid=[[[(-1 if not randint(0,4) else 0),0] for i in range(20)] for i in range(20)]
		number(self.grid)
		self.lost=False
		self.imgs=[load_pil_image(Image.open('mine.png')),load_pil_image(Image.open('cell.png'))]
	
	def draw(self):
		w=(1,)*3
		background(*w)
		if self.lost:
			tint(1,0,0)
			text('You Lose!', 'Helvetica', 36, *self.bounds.center())
			return
		global t_ct, t_type, t_loc, first
		push_matrix()
		translate(*self.bounds.center())
		imgs,dx,dy=self.imgs,self.dx,self.dy
		translate(dx,dy)
		scale(self.scale)
		touches=self.touches.values()
		stroke(*(.5,)*3)
		for y,i in enumerate(self.grid):
			for x,j in enumerate(i):
				fill(*(.8,)*3)
				stroke_weight(0.5)
				rect(20*x-1-200,20*y-1-200,20,20)
				tint(*w)
				k=j[1]
				j=j[0]
				if False:#not k:
					r=Rect(20*x-200-1,20*y-200-1,20,20)
					if t_loc in r:
						if t_type==0: tint(*(.7,)*3)
						if t_type==2:
							if first:
								for y1 in (y-1,y,y+1):
									for x1 in (x-1,x,x+1):
										self.grid[y1][x1][0]=0
								number(self.grid)
								first=False
							t_type=0
							self.auto(x,y)
					image(imgs[1],*r.as_tuple())
				elif j==-1:
					fill(1,0,0)
					rect(20*x-1-200,20*y-1-200,20,20)
					fill(*w)
					stroke_weight(0)
					rect(20*x+6-200,20*y+6-200,6,6)
					image(imgs[0],20*x+1.5-200,20*y+1.5-200,15,15)
				else:
					#image(imgs[1],20*x-1,20*y-1,20,20)
					tint(0,0,0)
					if j:
						text(str(j),'Courier',16,20*x+8.5-200,20*y+8.5-200)
		#self.update()
		pop_matrix()
		tint(0,0,0)
		#text(str(t_loc), 'Helvetica', 36, *self.bounds.center())
						
	def touch_began(self, touch):
		global t_ct, t_loc
		t_ct+=1
		if t_ct==1:
			t_loc=Point((touch.location.x-self.bounds.w/2-self.dx)/self.scale,(touch.location.y-self.bounds.h/2-self.dy)/self.scale)
			t_type=0
	
	def touch_moved(self, touch):
		global t_type, t_ct
		t_type=1
		self.dx+=(touch.location.x-touch.prev_location.x)/t_ct
		self.dy+=(touch.location.y-touch.prev_location.y)/t_ct

	def touch_ended(self, touch):
		global t_ct, t_type, t_loc
		t_ct-=1
		if t_ct==0:
			t_type=2
		
	def auto(self, x, y):# 3 0 6
		g=self.grid#         2   5
		adj=[0]*8 #          4 1 7
		if y>0:adj[0]=g[y-1][x]
		if y<len(g)-1:adj[1]=g[y+1][x]
		if x>0:
			adj[2]=g[y][x-1]
			if y>0:adj[3]=g[y-1][x-1]
			if y<len(g)-1:adj[4]=g[y+1][x-1]
		if x<len(g[y])-1:
			adj[5]=g[y][x+1]
			if y>0:adj[6]=g[y-1][x+1]
			if y<len(g)-1:adj[7]=g[y+1][x+1]
		self.grid[y][x][1]=1
		if g[y][x][0]==-1:
			self.lost=True
			return
		s=0
		for i in range(len(adj)):
			if adj[i][1]==1 or adj[i][1]==3:
				s+=1
				adj[i]=False
				if s>=g[y][x][0]:
					break
		for i in adj:
			if i!=False:
				if i==0:auto(x,y-1)
				if i==1:auto(x,y+1)
				if i==2:auto(x-1,y)
				if i==3:auto(x-1,y-1)
				if i==4:auto(x-1,y+1)
				if i==5:auto(x+1,y)
				if i==6:auto(x+1,y-1)
				if i==7:auto(x+1,y+1)

test=Game()

def testgrid():
	for i in test.grid:
		s=''
		for j in i:
			if len(str(j))==1:
				s+=' '
			s+=str(j)+' '
		print s
		
def regen():
	test.grid=[[-1 if not randint(0,4) else 0 for i in range(10)] for i in range(10)]

run(test)
