from scene import *
import os

class Map:
	def __init__(self, title, artist, creator, version, bpm, numobjs, cs, ar, od, hp, audiof, prevtime, bg, path):
		self.title=title
		self.artist=artist
		self.creator=creator
		self.version=version
		self.bpm=bpm
		self.numobjs=numobjs
		self.cs=cs
		self.ar=ar
		self.od=od
		self.hp=hp
		self.audiof=audiof
		self.prevtime=prevtime
		self.bg=bg
		self.path=path
		
	def __cmp__(self, other):
		return cmp(self.numobjs,other.numobjs)
		
	def __repr__(self):
		return self.artist+' - '+self.title+': '+self.version
		
class Mapset:
	def __init__(self, title, artist, creator, maps):
		self.title=title
		self.artist=artist
		self.creator=creator
		self.maps=maps
	
	def __cmp__(self,other):
		return cmp(self.title.lower(),other.title.lower())
	
	def __repr__(self):
		return self.artist+' - '+self.title+' by '+self.creator

class Picker (Scene):
	def setup(self):
		songs=[]
		for p in os.listdir('Songs'):
			maps=[]
			bpm=0
			for f in os.listdir('Songs/'+p):
				fail=0
				if f[-4:]=='.osu':
					bm=[l.strip() for l in open('Songs/%s/%s'%(p,f),'r').readlines()]
					#print bm
					for i,l in enumerate(bm):
						l=[j.strip() for j in l.split(':')]
						if l[0]=='Mode':
							if l[1]!='0':
								fail=1
								break
						if l[0]=='Title':
							title=l[1]
						if l[0]=='Artist':
							artist=l[1]
						if l[0]=='Creator':
							creator=l[1]
						if l[0]=='Version':
							version=l[1]
						if l[0]=='[HitObjects]':
							numobjs=len(bm[i+1:])
						if l[0]=='CircleSize':
							cs=float(l[1])
						if l[0]=='ApproachRate':
							ar=float(l[1])
						if l[0]=='HPDrainRate':
							hp=float(l[1])
						if l[0]=='OverallDifficulty':
							od=float(l[1])
						if l[0]=='PreviewTime':
							prevtime=float(l[1])/1000
						if l[0]=='AudioFilename':
							audiof=l[1]
						if l[0]=='//Background and Video events':
							bg=bm[i+1].split(',')[2][1:-1]
					if not fail:
						maps.append(Map(title, artist, creator, version, bpm, numobjs, cs, ar, od, hp, audiof, prevtime, bg, 'Songs/%s/'%p))
			songs.append(Mapset(title, artist, creator, list(sorted(maps))))
		self.songs=list(sorted(songs))
		
	def draw(self):
		# This will be called for every frame (typically 60 times per second).
		background(0, 0, 0)
		# Draw a red circle for every finger that touches the screen:
		fill(1, 0, 0)
		for touch in self.touches.values():
			ellipse(touch.location.x - 50, touch.location.y - 50, 100, 100)
	
	def touch_began(self, touch):
		pass
	
	def touch_moved(self, touch):
		pass

	def touch_ended(self, touch):
		pass

s=Picker()
run(s)
