# coding: utf-8

from scene import *
import sound
import random
import math
import colorsys
A = Action

class MyScene (Scene):
	def setup(self):
		self.h=0
	
	def did_change_size(self):
		pass
	
	def update(self):
		self.background_color=colorsys.hsv_to_rgb(self.h,1,1)
		self.h+=.2
		self.h%=1
	
	def touch_began(self, touch):
		pass
	
	def touch_moved(self, touch):
		pass
	
	def touch_ended(self, touch):
		pass

if __name__ == '__main__':
	run(MyScene(), show_fps=False)