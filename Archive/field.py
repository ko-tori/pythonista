from scene import *
import random

class MyScene (Scene):
	def setup(self):
		self.objs=[[1, 100,100],[-1, 400,100],[1, 700,100],[-1, 100,300]]
		self.stuff=[]
		self.v=0
		self.inp={}
	
	def draw(self):
		background(0, 0, 0)
		#text(str(self.inp), 'Helvetica', 36, *self.bounds.center())
		stroke_weight(0)
		for i,(q1,x,y,vx,vy) in enumerate(self.stuff):
			if q1>0:
				fill(1,0,0)
			elif q1<0:
				fill(0,0,1)
			else:
				fill(0,1,0)
			ellipse(x-5,y-5,10,10)
			self.stuff[i][1]+=vx
			self.stuff[i][2]+=vy
			fx=fy=0
			for q,x1,y1 in self.objs:
				d=((x1-x)**2+(y1-y)**2)**.5
				if d==0:
					fx=fy=0
				else:
					dx=x1-x
					dy=y1-y
					f=30*q/d**2
					fx+=f*dx
					fy+=f*dy
			self.stuff[i][3]-=fx*q1
			self.stuff[i][4]-=fy*q1
			
		for q,x,y in self.objs:
			if q>0:
				fill(1,0,0)
			elif q<0:
				fill(0,0,1)
			else:
				fill(0,1,0)
			ellipse(x-10,y-10,20,20)
		stroke_weight(1)
		stroke(1,1,1)
		for x in range(10,int(self.bounds.w),40):
			for y in range(10,int(self.bounds.h),40):
				fx=fy=0
				for q,x1,y1 in self.objs:
					d=((x1-x)**2+(y1-y)**2)**.5
					if d==0:
						fx=fy=0
					else:
						dx=x1-x
						dy=y1-y
						f=30*q/d**2
						fx+=f*dx
						fy+=f*dy
					
				m=(fx**2+fy**2)**.5
				stroke(1,1,1,m)
				fx*=10
				fy*=10
				if m!=0:
					line(x-fx/m,y-fy/m,x+fx/m,y+fy/m)
		#self.objs[0][1]+=1
		self.v+=1
	
	def touch_began(self, touch):
		a,b=touch.location
		for i,j in enumerate(reversed(self.objs)):
			q,x,y=j
			if abs(x-a)<=30 and abs(y-b)<=30:
				self.inp[touch.touch_id]=(0,len(self.objs)-i-1)
				break
		else:
			for i,j in enumerate(reversed(self.stuff)):
				q,x,y,vx,vy=j
				if abs(x-a)<=15 and abs(y-b)<=15:
					self.inp[touch.touch_id]=(1,len(self.objs)-i-1)
					break
			else:
				self.stuff.append([random.randint(0,1)*2-1,a,b,0,0])

	def touch_moved(self, touch):
		if touch.touch_id in self.inp:
			i=self.inp[touch.touch_id]
			[self.objs,self.stuff][i[0]][i[1]][1:]=list(touch.location)

	def touch_ended(self, touch):
		if touch.touch_id in self.inp:
			i=self.inp[touch.touch_id]
			[self.objs,self.stuff][i[0]].append([self.objs,self.stuff][i[0]].pop(i[1]))
			del self.inp[touch.touch_id]
			self.inp={k:(v,(w-1 if j>i[1]-2 else w)) for j,(k,(v,w)) in enumerate(list(self.inp.iteritems()))}

a=MyScene()
run(a)
