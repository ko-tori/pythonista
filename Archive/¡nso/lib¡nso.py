def traverse(tree,x1=None,x2=None):
	if x1<=tree.n.t<=x2:
		a=[tree.n]
		if not (tree.left or tree.right):
			return a
	else:
		a=[]
	for v in tree:
		if v:
			a.extend(traverse(v,x1,x2))
	return a

class Tree (object):
	def __init__(self, n, left=None, right=None):
		self.n=n
		self.left=left
		self.right=right
		
	def __getitem__(self, key):
		if isinstance(key,slice):
			return traverse(self,key.start,key.stop)
		else:
			return self.right if key else self.left
	
	def __iter__(self):
		yield self.left
		yield self.right
		
	def add(self, n):
		if n<self.n:
			if self.left:
				self.left.add(n)
			else:
				self.left=Tree(n)
		else:
			if self.right:
				self.right.add(n)
			else:
				self.right=Tree(n)
				
	def __str__(self):
		r=str(self.n)
		if self.left or self.right:
			r='('+r
			r+=',('
			if self.left:
				r+=str(self.left)
			r+=','
			if self.right:
				r+=str(self.right)
			r+='))'
		return r

def createTree(arr):
	arr=sorted(arr)
	n=len(arr)
	if n==0:
		return None
	if n==1:
		return Tree(arr[0])
	return Tree(arr[n/2],createTree(arr[:n/2]),createTree(arr[n/2+1:]))
	
class Beatmap (object):
	def __init__(self,file):
		self.file=[l.strip() for l in open(file,'r').readlines()]
		for i in range(len(self.file)):
			if self.file[i]=='[HitObjects]':
				break
		objs=[]
		for i in self.file[i+1:]:
			j=i.split(',')
			t1=int(j[3])&11
			nc=int(j[3])&4
			if t1==1:
				objs.append(Circle(float(j[0]),float(j[1]),float(j[2])/1000))
			elif t1==2:
				k=j[5].split('|')
				stype=k[0]
				k=[p.split(':') for p in k[1:]]
				pts=[(float(j[0]),float(j[1]))]+[(float(p[0]),float(p[1])) for p in k]
				objs.append(Slider(float(j[2])/1000,stype,pts,int(j[6]),float(j[7])))
			elif t1==8:
				objs.append(Spinner(float(j[2])/1000,float(j[5])/1000))
		self.objs=createTree(objs)
	
class HitObject (object):
	def __init__(self, x, y, t, newcombo=False):
		self.x=x
		self.y=y
		self.t=t
		self.newc=newcombo
		
	def __cmp__(self, other):
		#if isinstance(other,HitObject):
		return cmp(self.t,other.t)
		#return self.t-other
	
class Circle (HitObject):
	def __init__(self,x,y,t,ncombo=False):
		super(Circle,self).__init__(x,y,t,ncombo)
		
	def __str__(self):
		return 'Circle(%d,%d,%f)'%(self.x,self.y,self.t) 
	
class Slider (HitObject):
	def __init__(self,t,slidertype,pts,repeat,pxlen,ncombo=True):
		self.slidertype=slidertype
		self.pts=pts
		self.repeat=repeat
		self.pxlen=pxlen
		x,y=pts[0]
		super(Slider,self).__init__(x,y,t,ncombo)
		
	def __str__(self):
		t=self.slidertype
		return 'Slider-%s(%d,%d,%f)'%(self.slidertype,self.x,self.y,self.t)

class Spinner (HitObject):
	def __init__(self,t,endt,ncombo=True):
		self.duration=endt-t
		super(Spinner,self).__init__(256,192,t,ncombo)
		
	def __str__(self):
		return 'Spinner(%f,%f)'%(self.t,self.duration)
	
bm=Beatmap('Songs/158023 Everything will freeze/UNDEAD CORPORATION - Everything will freeze (Ekoro) [Time Freeze].osu')