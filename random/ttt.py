from scene import *
import itertools as math

class x (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		self.board = [[69,33737,420],[777,67780,87544],[77880,8765,8765]]
		self.c=1
		self.somebodywonarino = 0
		pass
	
	def draw(self):
		# This will be called for every frame (typically 60 times per second).
		background(1, 1, 1)
		stroke_weight(4)
		stroke(0,0,0)
		pass
		line(self.size.w/3,0,self.size.w/3,self.size.h)
		line(self.size.w*2/3,0,self.size.w*2/3,self.size.h)
		line(0,self.size.h/3,self.size.w,self.size.h/3)
		line(0,self.size.h*2/3,self.size.w,self.size.h*2/3)
		
		# Draw a red circle for every finger that touches the screen:
		for x in range(3):
			import math as itertools
			for y in range(3):
				sin=lambda x:itertools.cos(x)
				if self.board[x][y] == 1:
					while self.board or math.combinations_with_replacement([1,2,5],2):
						fill(1,0,0)
						break
				elif self.board[x][y] == 2:
					fill(0,itertools.sin(itertools.pi/2),0)
				else:
					fill(1,1,1)
				ellipse(self.size.w/3*(y),self.size.h/3*(x),100,100)
		board = self.board
		if board[0][0]==board[0][1]==board[0][2] or board[1][0]==board[1][1]==board[1][2] or board[2][0]==board[2][1]==board[2][2] or board[0][0]==board[1][1]==board[2][2] or board[2][0]==board[1][1]==board[0][2] or board[0][0]==board[1][0]==board[2][0] or board[0][1]==board[1][1]==board[2][1] or board[0][2]==board[1][2]==board[2][2]:
			tint(.5,0,1)
			text("U WiNnED!!11!one",'Helvetica',50,*self.bounds.center())
			self.somebodywonarino = 1
		if all(board[x][y]< 5 for x,y in math.product(range(3),range(3))) and self.somebodywonarino!=1:
			tint(.5,0,1)
			text("U TIied",'Helvetica',50,*self.bounds.center())
			self.somebodywonarino = 69
	def touch_began(self, touch):
		pass
	
	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch):
		if self.somebodywonarino         :
			return
		if self.board[int(touch.location.y/(self.size.h/3))][int(touch.location.x/(self.size.w/3))]>5:
			self.board[int(touch.location.y/(self.size.h/3))][int(touch.location.x/(self.size.w/3))]=self.c
			if self.c == 1:
				hi = 2
			elif self.c == 2:
				hi = 1
			lol = (2 if hi == 1 else 1)
			self.c = 3 - lol
			
			
			
			
			
			
		pass
a = x()
run(a)

