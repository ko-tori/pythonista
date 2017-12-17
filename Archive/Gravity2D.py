from scene import *
from random import *
from itertools import *

G=500
drawPath=False
refFrame=False
focus=1
sun=1
randMov=True
killDist=None
#killDist=1000
indicators=False

class Planet():
	def __init__(self, x, y, size, mass, xvel=None, yvel=None, color=Color(1,1,1), lum=1):
		self.x=x
		self.y=y
		self.size=size
		self.mass=mass
		self.xvel=xvel
		self.yvel=yvel
		self.color=color
		self.lum=lum
		if drawPath: self.path=[Point(x,y)]
		if randMov:
			self.xvel=randint(-100,100) if xvel==None else xvel
			self.yvel=randint(-100,100) if yvel==None else yvel
		else:
			self.xvel=0 if xvel==None else xvel
			self.yvel=0 if yvel==None else yvel
		self.delflag=False
		
	def update(self, dt):
		self.x+=self.xvel*dt
		self.y+=self.yvel*dt
		#print self.xvel, self.yvel
		
	def force(self, x, y, dt):
		self.xvel+=x*dt/self.mass
		self.yvel+=y*dt/self.mass
		#print "Force (",x,',',y,')'

class MyScene (Scene):
	def setup(self):
		self.center=self.bounds.center()
		self.planets=[]
		if sun: self.planets.append(Planet(0,0,10,5000,0, 0,Color(1,1,0),5))
		#pl=Planet(50,0, 7, 10, 0, 400)
		#self.planets.append(pl)
		#pl=Planet(-200,0, 5, 5, 100, 120)
		#self.planets.append(pl)
		self.mode=0
		self.ct=0
		self.scale=1
		self.spt=Point(0,0)
		self.zcenter=Point(0,0)
	
	def draw(self):
		if refFrame:
			global focus
			try:
				push_matrix()
				translate(-self.planets[focus].x, -self.planets[focus].y)
			except:
				pass
		background(0, 0, 0)
		tint(1,0,0)
				
		if drawPath:
			stroke_weight(0.5)
			for p in self.planets:
				stroke(*p.color)
				for i in xrange(1,len(p.path)):
					line(*self.T(p.path[i].x, p.path[i].y, p.path[i-1].x, p.path[i-1].y))
		for p in self.planets:
			if abs(p.x)+abs(p.y)>killDist and killDist: 
				del p
				continue
			r=p.size
			for aa in xrange(100,0,-100/p.lum):
				fill(p.color.r,p.color.g,p.color.b, aa/100.)
				stroke(p.color.r,p.color.g,p.color.b, aa/100.)
				ellipse(*self.T(p.x-r/2,p.y-r/2,r))
				r+=2
			p.update(self.dt)
			if drawPath and p.xvel>0 and p.yvel>0:
				p.path.append(Point(p.x, p.y))
		for i in combinations(self.planets, 2):
			if abs(i[0].x-i[1].x)+abs(i[0].y-i[1].y)>1000: continue
			#i=list(i)
			if abs((i[1].size/2.+i[0].size/2.)-((i[1].x-i[0].x)**2+(i[1].y-i[0].y)**2)**0.5)<=5:
				if i[1].mass>i[0].mass: i=i[::-1]
				i[0].size+=(i[1].size/2.)**2/(i[0].size)
				i[0].mass+=i[1].mass
				i[0].xvel=(i[0].mass*i[0].xvel+i[1].mass*i[1].xvel)/(i[1].mass+i[0].mass)
				i[0].yvel=(i[0].mass*i[0].yvel+i[1].mass*i[1].yvel)/(i[1].mass+i[0].mass)
				i[1].delflag=True
				continue
			c=((i[0].x-i[1].x)**2+(i[0].y-i[1].y)**2)**0.5
			gc=i[0].mass*i[1].mass*G/c**3
			self.fgdt=fgdt=(gc*(i[0].x-i[1].x), gc*(i[0].y-i[1].y), self.dt)
			i[0].force(*fgdt)
			i[1].force(*fgdt)
		self.planets=[i for i in self.planets if not i.delflag]
		
		if indicators:
			text('+', 'Helvetica', 12, *self.T(0,0))
			if killDist:
				stroke(1,0,0)
				stroke_weight(0.4)
				line(*self.T(-killDist,0,0,-killDist, True))
				line(*self.T(0,-killDist,killDist,0, True))
				line(*self.T(killDist,0,0,killDist, True))
				line(*self.T(0,killDist,-killDist,0, True))
				
		#translate(self.planets[focus].x-self.center.x, self.planets[focus].y-self.center.y)
		if refFrame: pop_matrix()
		#translate(-self.center.x, -self.center.y)
		fill(1,1,1)
		#self.roundrect(30,30,100,60,10)
		#text('Origin: ' + str(self.center),'Helvetica',16,*self.bounds.center(),alignment=8)
		#text('Zoom origin: ' + str(self.zcenter),'Helvetica',16,*self.bounds.center(),alignment=2)
	
	def touch_began(self, touch):
		t=self.touches.values()
		self.ct+=1
		if self.ct==1:
			self.spt=Point(touch.location.x, touch.location.y)
	
	def touch_moved(self, touch):
		#print touch.location.x-self.center.x
		#print touch.location
		#pop_matrix()
		#translate(self.center.x, self.center.y)
		#scale(4**self.scale-1)
		t=self.touches.values()
		if len(t)==2:
			dscale=(t[1].location.distance(t[0].location)-t[1].prev_location.distance(t[0].prev_location))/500
			if not(self.scale<0.05 and dscale<0): self.scale+=dscale
			self.center.x+=(t[1].location.x-t[1].prev_location.x+t[0].location.x-t[0].prev_location.x)/2
			self.center.y+=(t[1].location.y-t[1].prev_location.y+t[0].location.y-t[0].prev_location.y)/2
			self.zcenter=Point(((t[1].location.x+t[0].location.x)/2-self.center.x), ((t[1].location.y+t[0].location.y)/2-self.center.y))
			#self.center=Point(((t[1].location.x+t[0].location.x)/2), ((t[1].location.y+t[0].location.y)/2))
		if len(t)==1:
			#print self.spt
			stroke_weight(20)
			stroke(1,1,1)
			#line(0,0,100,100)
			line(*self.T(self.spt.x, self.spt.y, touch.location.x, touch.location.y))

	def touch_ended(self, touch):
		#pop_matrix()
		#scale(4**self.scale-1)
		if self.ct==1:
			global focus, refFrame
			x=y=0
			try:
				x=self.planets[focus].x if refFrame else 0
				y=self.planets[focus].y if refFrame else 0
			except:
				pass
			self.planets.append(Planet(*self.T(touch.location.x+x, touch.location.y+y, 5, 10, False)))
		if len(self.touches.values())==0:
			self.ct=0
		#self.zcenter=self.center
		
	def roundrect(self, x, y, w, h, r):
		if 2*r>h: r=h/2
		if 2*r>w: r=w/2
		rect(x+r, y, w-2*r, h)
		rect(x, y+r, w, h-2*r)
		ellipse(x, y, 2*r, 2*r)
		ellipse(x, y+h-2*r, 2*r, 2*r)
		ellipse(x+w-2*r, y, 2*r, 2*r)
		ellipse(x+w-2*r, y+h-2*r, 2*r, 2*r)
		
	def T(self,x,y,r=None,r2=None, p=True):
		s=self.scale
		z=self.zcenter
		c=self.center
		if r is None:
			return s*(x-z.x)+c.x+z.x,s*(y-z.y)+c.y+z.y
		if r2 is None:
			return s*(x-z.x)+c.x+z.x,s*(y-z.y)+c.y+z.y,r*s,r*s
		if p:
			return (s*(x-z.x)+c.x+z.x,s*(y-z.y)+c.y+z.y,s*(r-z.x)+c.x+z.x,s*(r2-z.y)+c.y+z.y)
		return (x-z.x-c.x)/s+z.x,(y-z.y-c.y)/s+z.y,r,r2

dbg=MyScene()
run(dbg)
