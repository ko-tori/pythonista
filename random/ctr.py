from scene import *

class MyScene (Scene):
	def setup(self):
		self.p=4
		self.m=[10]*(self.p-1)+[0]
	
	def draw(self):
		background(1,1,1)
		tint(0,0,0)
		stroke_weight(1)
		stroke(0,0,0)
		line(0,self.bounds.h/2-24,self.bounds.w,self.bounds.h/2-24)
		line(0,self.bounds.h/2+24,self.bounds.w,self.bounds.h/2+24)
		for i in range(1,self.p):
			line(i*self.bounds.w/self.p,0,i*self.bounds.w/self.p,self.bounds.h+36)
		for x in range(0,self.p):
			text(str(self.m[x]), 'Helvetica', 36, x*self.bounds.w/self.p+self.bounds.w/self.p/2,self.bounds.h/2,5)

	def touch_ended(self, touch):
		n=int(touch.location.x/(self.bounds.w+1)*self.p)
		if touch.location.y>self.bounds.h/2+24:
			a=1
		elif touch.location.y<self.bounds.h/2-24:
			a=-1
		else:
			a=0
		self.m[n]+=a

test=MyScene()
run(test)
