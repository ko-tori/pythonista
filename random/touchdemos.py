from scene import *
from itertools import combinations
from random import random

class Scene1 (Scene):
	def draw(self):
		background(0, 0, 0)
		stroke_weight(3)
		for i,j in combinations(self.touches.values(),2):
			stroke(1,0,0,.5)
			n=random()
			stroke_weight(n*3+2)
			line(i.location.x,i.location.y,j.location.x,j.location.y)
			
class Scene2 (Scene):
	def setup(self):
		self.c=0
		
	def draw(self):
		background(self.c,0,0)
		self.c*=.95
		
	def touch_began(self, touch):
		self.c=1
			
run(Scene1())

