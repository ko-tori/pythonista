from scene import *
from motion import *

class MyScene (Scene):
	def setup(self):
		start_updates()
		self.rotv=[0,0,0]
		self.rot=[0,0,0]
	
	def draw(self):
		translate(*self.bounds.center())
		background(0,0,0)
		m=get_gravity()
		for i in range(3):
			self.rotv[i]-=m[i]/3
			self.rot[i]-=self.rotv[i]
		push_matrix()
		rotate(self.rot[1])
		fill(1,0,0)
		rect(-50,-50,100,100)
		pop_matrix()
		tint(1,1,1)
		text(str(self.rotv[1]))
	
	def touch_began(self, touch):
		pass
	
	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch):
		pass

run(MyScene())
