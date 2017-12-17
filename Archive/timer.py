from scene import *
from time import *

t=time()

class Timer (Scene):
	def setup(self):
		self.on=False
		self.temp=0.0
	
	def draw(self):
		background(0,0,0)
		global t
		if self.on:
			text(str(time()-t), 'Helvetica', 36, *self.bounds.center())
		else:
			text(str(self.temp), 'Helvetica', 36, *self.bounds.center())
	
	def touch_began(self, touch):
		global t
		if self.on==True:
			self.temp=time()-t
		t=time()
		self.on=(not self.on)

a=Timer()
run(a)
