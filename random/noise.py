from scene import *
from random import *

res=8

def eq1(a,b):
	a=sum(abs(i-j) for i,j in zip(a,b))<.9
	#print a
	return a

class MyScene (Scene):
	def setup(self):
		self.arr=[[(random(),random(),random()) for i in xrange(int(self.bounds.w/res))] for j in xrange(int(self.bounds.h/res))]
		self.loc=None
		self.w,self.h=len(self.arr[0]),len(self.arr)
		#self.lines=
	
	def draw(self):
		stroke_weight(0)
		for i in xrange(len(self.arr)):
			for j in xrange(len(self.arr[0])):
				fill(*self.arr[i][j])
				rect(res*j,res*i,res,res)
		if self.loc:
			l=self.loc
			stroke(*self.arr[l[1]][l[0]])
			stroke_weight(5)
			for i in range(10):
				x,y=(self.loc[0]+randint(-5,5)*res)%(self.w),(self.loc[1]+randint(-5,5)*res)%(self.h)
				x,y=int(x),int(y)
				#print x,y,l
				if eq1(self.arr[l[1]][l[0]],self.arr[y][x]):
					self.arr[y][x]=self.arr[l[1]][l[0]]
					line(res*l[0],res*l[1],x*res,y*res)
					self.loc=x,y
	
	def touch_began(self, touch):
		if self.loc is None:
			self.loc=int(touch.location.x/res),int(touch.location.y/res)
	
	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch): 
		pass

a=MyScene()
run(a)
