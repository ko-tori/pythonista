# coding: utf-8

import ui
from random import randint

class Draw(ui.View):
	def __init__(self):
		self.imgs=[ui.Image.named('mine.png'),ui.Image.named('cell.png')]
		self.dx=0
		self.dy=0
	def did_load(self):
		self.t=ui.Transform.translation(*self.bounds[2:])
		self.touches=[]
		self.grid=[[-1 if not randint(0,3) else 0 for i in range(25)] for i in range(25)]
	
	def draw(self):
		imgs=self.imgs
		dx=self.dx%100
		dy=self.dy%100
		touches=self.touches
		
				
	def touch_began(self, touch):
		self.touches.append(touch)
		
	def touch_moved(self, touch):
		self.dx+=(touch.location[0]-touch.prev_location[0])/len(self.touches)
		self.dy+=(touch.location[1]-touch.prev_location[1])/len(self.touches)
		self.set_needs_display()
		
	def touch_ended(self, touch):
		self.touches.remove(touch)

ms=ui.load_view('ms')
a=ms['canvas']
ms.present('full_screen')
