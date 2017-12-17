from scene import *

class MyScene (Scene):
	def setup(self):
		self.x=0
		self.y=0
		self.zoom=1
		self.c=(0,0)
	
	def draw(self):
		translate(*self.bounds.center())
		fill(1,1,1)
		background(0,0,0)
		translate(self.x, self.y)
		push_matrix()
		translate(-self.bounds.center().x,-self.bounds.center().y)
		translate(*self.c)
		scale(self.zoom)
		rect(-10,10,20,20)
		try:
			text(str(self.c), 'Helvetica', 36, 0,0)
		except:
			pass
	
	def touch_began(self, touch):
		pass
	
	def touch_moved(self, touch):
		if len(self.touches.values())==1:
			self.x+=touch.location.x-touch.prev_location.x
			self.y+=touch.location.y-touch.prev_location.y
		if len(self.touches.values())==2:
			t=self.touches.values()
			dist=t[0].location.distance(t[1].location)
			prev=t[0].prev_location.distance(t[1].prev_location)
			self.c=((t[0].location.x-t[1].location.x)/2,(t[0].location.y-t[1].location.y)/2)
			self.zoom+=(dist-prev)/100.
			self.zoom=.1 if self.zoom<.1 else (3 if self.zoom>3 else self.zoom)

	def touch_ended(self, touch):
		pass

run(MyScene())
