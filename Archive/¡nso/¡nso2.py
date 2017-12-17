#coding: utf-8

'''
To do:
Everything
'''

import music
import sound,math,re,time
from threading import Thread,Timer
from scene import *
import ui,io
from PIL import Image, ImageOps as IOps
import sliderlib2 as sliderlib

A=Action
eo=TIMING_EASE_OUT_2

def cs(n):
	return 88-8*(n-2)

def ar(n):
	return round(1.2-((n-5)*.15 if n>=5 else (n-5)*.12),4)

class Osu(Scene):
	def __init__(self, song, folder, mods=0):
		self.song=song
		self.folder='Songs/'+folder
		self.mod_hr=mods&1
		self.mod_ez=mods&2
		self.mod_hd=mods&4
		self.mod_ht=mods&8
		self.mod_dt=mods&16
	
	def setup(self):
		self.bm=[l.strip() for l in open(self.folder+'/'+self.song,'r').readlines()]
		self.cols=[]
		for i,j in enumerate(self.bm):
			if j[:13]=='ApproachRate:':
				self.ar=ar(min(10,float(j[13:])*(1.4 if self.mod_hr else (.5 if self.mod_ez else 1))))/(1.5 if self.mod_dt else .75 if self.mod_ht else 1)
			if j[:11]=='CircleSize:':
				self.cs=cs(min(10,float(j[11:])*(1.4 if self.mod_hr else (.5 if self.mod_ez else 1))))
			if j[:15]=='AudioFilename: ':
				audiofile=self.audiofile=self.folder+'/'+j[15:]
			if j[:14]=='StackLeniency:':
				stackl=float(j[14:])
			if j[:13]=='AudioLeadIn: ':
				self.leadin0=self.leadin=float(j[13:])/1000
			if j[:17]=='SliderMultiplier:':
				self.sliderx=sliderx=float(j[17:])*(1.5 if self.mod_dt else .75 if self.mod_ht else 1)
			if j[:15]=='SliderTickRate:':
				self.tickrate=float(j[15:])
			r=re.sub('Combo\d : ','',j)
			if r!=j:
				self.cols.append(tuple(float(k)/255 for k in r.split(',')))
			if j=='//Background and Video events':
				bgpic=self.bm[i+1].split(',')[2][1:-1]
			if j=='//Break Periods':
				if self.bm[i+1][0]=='/':
					self.breaks=[]
				else:
					self.breaks=[float(k)/1000 for k in self.bm[i+1].split(',')]
			if j=='[TimingPoints]':
				timingi=i+1
			if j=='[HitObjects]':
				break
		if not self.cols:
			self.cols=[(1.,192./255,0.),(0.,202.,0.),(18./255,124./255,1.),(242./255,24./255,57./255)]
		self.tpts=[]
		for l in self.bm[timingi:i]:
			if l=='[Colours]' or l=='':
				break
			stuff=[float(a) for a in l.split(',') if a]
			if stuff[6]==0 and self.tpts:
				stuff[6]=self.tpts[-1][0]
			else:
				stuff[6]=stuff[0]
			self.tpts.append((stuff[0]/1000.,stuff[1]/1000 if stuff[1]>0 else self.tpts[-1][1],-100./stuff[1] if stuff[1]<0 else 1,stuff[6],stuff[7]==1))
		#tpts[n]=[time,beatlength,velocity,lasttime,kiai]
		self.tptn=0
		self.objs=[i.split(',') for i in self.bm[i+1:]]
		self.ct=len(self.objs)
		self.ts=[int(i[2])/1000. for i in self.objs]
		self.x=[float(i[0]) for i in self.objs]
		self.y=[(float(i[1]) if self.mod_hr else 384-float(i[1])) for i in self.objs]
		otypes=[(int(i[3])&11,int(i[3])&4) for i in self.objs]
		self.hitdata=[[-1,0]] #[hit time, hit type] hit types: 0: not hit yet, 1: 300, 2: 100, 3: 50, 4: miss
		self.disp=[0]*self.ct
		
		#self.cols=[(1,1,1)]
		self.cols=[(200/255.,200/255.,1),(0,1,100/255.),(200/255.,100/255.,100/255.),(100/255.,1,100/255.)]
		
		#Parse Object Types and Colors
		self.otypes=[]
		n=0
		n2=1
		for i,j in otypes:
			if j:
				n+=1
				n%=len(self.cols)
				n2=1
			self.otypes.append((i,n,n2))
			n2+=1
				
		#Stacking
		prev=self.x[0],self.y[0]
		tprev=self.ts[0]
		n=0
		stacks=[0]*self.ct
		for i in range(1,self.ct):
			if (self.x[i],self.y[i])==prev and self.ts[i]-tprev<stackl/2:
				n+=1
				stacks[i]=n
			else:
				n=0
			prev=self.x[i],self.y[i]
			tprev=self.ts[i]
		for i in range(self.ct):
			self.x[i]+=stacks[i]*self.cs/24
			self.y[i]-=stacks[i]*self.cs/24
			
		#Sliders
		self.sd=[]
		self.si={}
		n=0
		for i,j in enumerate(self.objs):
			if self.otypes[i][0]==2:
				t=float(j[2])/1000
				while n<len(self.tpts)-1 and self.tpts[n+1][0]<=t:
					n+=1
				c=j[5].split('|')
				t=c[0]
				c=[k.split(':') for k in c[1:]]
				c=[(self.x[i],self.y[i])]+[(float(k[0]),(float(k[1]) if self.mod_hr else 384-float(k[1]))) for k in c]
				l=float(j[7])
				if t=='L':
					p=sliderlib.line(c,l)[0]
				if t=='B':
					p=sliderlib.bezier(c,l)
				if t=='P':
					p=sliderlib.passthrough(c,l)
				pxpb=sliderx*100*self.tpts[n][2]
				r=int(j[6])
				sbl=r*l/pxpb
				self.sd.append([p,sbl*self.tpts[n][1],r,n,l,pxpb/self.tickrate,self.tpts[n][1]/self.tickrate])
				self.si[i]=0
				#sd[n]=[data,duration,repeats,timingpoint#,pxlen,px/tick,tick interval]
				#si[n]=[image, pos]
			else:
				self.sd.append(0)
		#self.slideredge=(1,1,1)
		self.slideredge=(200/255.,)*3
		#self.sliderfill=None
		self.sliderfill=(0,0,0)
		self.i=0
		self.stopped=False
		self.paused=False
		self.background_color=(0,0,0)
		self.a=Node((128,99),scale=1.5)
		self.add_child(self.a)
		#self.test=SpriteNode(position=self.bounds.center())
		#self.add_child(self.test)
		self.tlabel=LabelNode('0',('TrebuchetMS',12),position=(0,0))
		self.tlabel.anchor_point=(0,0)
		self.add_child(self.tlabel)
		
		self.bgdim=.75
		self.bgdim=max(1-self.bgdim,.001)
		try:
			self.bg=bg=IOps.fit(Image.open(self.folder+'/'+bgpic,).convert('RGBA'),(1024,748),1)
			with io.BytesIO() as bIO:
				bg.save(bIO,'PNG')
				bg=ui.Image.from_data(bIO.getvalue())
			self.bg=SpriteNode(Texture(bg),self.bounds.center(), -1, alpha=.5)
			self.add_child(self.bg)
		except:
			self.bg=Node()
		Thread(target=self.load_sliders).start()
		time.sleep(self.ar*2)
		self.player=music.Player(audiofile,(1.5 if self.mod_dt else .75 if self.mod_ht else 1))
		Timer(self.leadin,self.playsong).start()
		
	def update(self):
		t=self.player.current_time()-self.leadin+(.2+(.2if self.mod_ez else 0) if self.mod_dt else 0)
		ar,cs=self.ar,self.cs
		ts,x,y,ots,sd=self.ts,self.x,self.y,self.otypes,self.sd
		self.tlabel.text=str(t-ts[0])
		#self.test.scale=self.getbeat()
		#if self.breaks:print t,self.breaks[0]
		if self.i==0 and t+.8>=ts[0]:
				self.bg.run_action(A.fade_to(self.bgdim,1))
		if self.breaks and t>=self.breaks[0]:
			c=SpriteNode('Skin/Section-%s.png'%('pass' if 1 else 'fail'),position=(256,198),scale=.5,alpha=.001)
			dt=ts[self.i]-ar-self.breaks[0]
			#print dt
			if 0:#len(self.breaks)>1 and ts[self.i]>self.breaks[1]:
					dt=ts[self.i]-ar-self.breaks[1]
					#print dt
					del self.breaks[0]
			if dt>1 and self.i>0:
				c.run_action(A.sequence(A.wait(dt/2-.2),A.fade_to(1,0),A.wait(.1),A.fade_to(.001,0),A.wait(.1),A.fade_to(1,0),A.wait(1),A.fade_to(0,.1)))
				self.a.add_child(c)
			if dt>2.5 or self.i==0:
				self.bg.run_action(A.sequence(A.fade_to(max(self.bgdim,.5),1),A.wait(dt-1.8),A.fade_to(self.bgdim,1)))
			del self.breaks[0]
		while self.tptn<len(self.tpts)-1 and self.tpts[self.tptn+1][0]<=t:#timing point number
			self.tptn+=1
		a1hd=A.sequence(A.fade_to(1,ar/2),A.fade_to(0,ar/4))
		a1=A.sequence(A.fade_to(1,ar/2),A.wait(ar/2),A.group(A.fade_to(0,.25),A.scale_by(.1,.25)))
		while self.i<self.ct and ts[self.i]<=t+ar:
			i=self.i
			if 0:#i<self.ct-1 and ots[i+1][2]!=1:
				x1,y1=(sd[i][0][-1] if ots[i][0]==2 else (x[i],y[i]))
				x2,y2=x[i+1],y[i+1]
				dx,dy=x2-x1,y2-y1
				m=(dx**2+dy**2)**.5
				if m>2*cs:
					o=ui.Path()
					o.line_width=2
					o.move_to(x1+dx/m*cs/2,y2-(y1+dy/m*cs/2))
					o.line_to(x2-dx/m*cs/2,dy/m*cs/2)
					c=ShapeNode(o,stroke_color=(.2,.5,1),position=((x1+x2)/2,(y1+y2)/2),z_position=-t*2,alpha=.001)
					c.run_action(A.sequence(A.wait(ts[i+1]-ts[i]),A.fade_to(1,ar),A.fade_to(0,ar/2)))
					self.a.add_child(c)
			if ots[i][0]==8:
				b=Node((256,192),alpha=.001)
				c=SpriteNode('Skin/spinner-approachcircle.png')
				b.add_child(c)
				b.run_action(A.sequence(A.wait(ar-.25),A.fade_to(1,.25),A.scale_to(0,(float(self.objs[i][5])/1000.-ts[i])/(1.5 if self.mod_dt else .75 if self.mod_ht else 1)),A.fade_to(0,0)))
				self.disp[i]=[8,b]
				self.a.add_child(b)
			else:
				col=self.cols[self.otypes[self.i][1]]
				b=Node((x[i],y[i]),-t,cs/128.,alpha=0)
				c=SpriteNode('Skin/hitcircle.png',color=col)
				b.add_child(c)
				c=SpriteNode('Skin/hitcircleoverlay.png')
				b.add_child(c)
				n=str(self.otypes[self.i][2])
				l=len(n)
				w=.8*cs/1.5
				off=-(l-1)/2.*w
				for k in n:
					c=SpriteNode('Skin/default-%s.png'%k,position=(off,0),scale=cs/71*.8)
					b.add_child(c)
					off+=w
				b.run_action(a1hd if self.mod_hd else a1)
				self.a.add_child(b)
				if self.i==0 or not self.mod_hd:
					c=SpriteNode('Skin/approachcircle.png',(x[i],y[i]),-t,cs/128.*3,color=col,alpha=0)
					c.run_action(A.sequence(A.group(A.fade_to(1,ar/2),A.scale_to(cs/128.,ar)),A.fade_to(0,0)))
					self.a.add_child(c)
				self.disp[i]=[ots[i][0],b]
				if ots[i][0]==2:
					img,pos=self.si[i]
					c=SpriteNode(Texture(img),pos,-t-.001,alpha=.001)
					#del self.si[i]
					c.anchor_point=(0,0)
					sdur=sd[i][1]
					if self.mod_hd:
						c.run_action(A.sequence(A.fade_to(.8,ar/2),A.fade_to(.5,ar/2),A.fade_to(0,sdur*.75)))
					else:
						c.run_action(A.sequence(A.fade_to(.8,ar/2),A.wait(ar/2+sdur),A.fade_to(0,.25)))
					self.a.add_child(c)
					pts=sd[i][0]
					self.pts=pts
					r=sd[i][2]
					def f_ra(node,prog):
						node.scale=cs/128+self.getbeat()/5
					for rn in range(r-1):
						if rn==0:
							angle=math.atan2(pts[-3][1]-pts[-2][1],pts[-3][0]-pts[-2][0])
							c=SpriteNode('Skin/reverse-arrow.png',position=pts[-1],scale=cs/128,alpha=.001)
							c.rotation=angle
							if self.mod_hd:
								c.run_action(A.group(A.call(f_ra,ar+sdur/r+.25),A.sequence(A.fade_to(1,ar),A.wait(sdur/r),A.group(A.fade_to(0,.2),A.scale_by(.1,.2)))))
							else:
								c.run_action(A.group(A.call(f_ra,ar+sdur/r+.25),A.sequence(A.fade_to(1,ar/2),A.wait(sdur/r+ar/2),A.group(A.fade_to(0,.2),A.scale_by(.1,.2)))))
							self.a.add_child(c)
						else:
							if rn%2:
								angle=math.atan2(pts[1][1]-pts[0][1],pts[1][0]-pts[0][0])
								c=SpriteNode('Skin/reverse-arrow.png',position=pts[0],scale=cs/128,alpha=.001)
							else:
								angle=math.atan2(pts[-3][1]-pts[-2][1],pts[-3][0]-pts[-2][0])
								c=SpriteNode('Skin/reverse-arrow.png',position=pts[-1],scale=cs/128,alpha=.001)
							c.rotation=angle
							c.run_action(A.sequence(A.wait(ar+sdur/r*(rn-1)),A.group(A.call(f_ra,sdur/r*2),A.sequence(A.fade_to(1,0),A.wait(sdur/r*2))),A.group(A.fade_to(0,.2),A.scale_by(.1,.2))))
							self.a.add_child(c)
					b=Node((x[i],y[i]),-t+.1,alpha=0.01)
					p=ui.Path.oval(0,0,15.*cs/18,15.*cs/18)
					p.line_width=cs/15.
					c=SpriteNode('Skin/sliderb0.png',scale=cs/128)
					b.add_child(c)
					if 1:
						c=SpriteNode('Skin/sliderfollowcircle.png',scale=cs/259.)
						c.run_action(A.sequence(A.wait(ar-.1),A.scale_to(2*cs/259.,.1),A.wait(sdur),A.scale_to(cs/259.,.1)))
						self.disp[i].append(c)
						b.add_child(c)
					l=sd[i][4]
					dp=[0]
					s=0
					n=0
					pxpt=sd[i][5]
					beatlen=sd[i][6]
					ticks=[]
					for j in range(1,len(pts)):
						dx=pts[j][0]-pts[j-1][0]
						dy=pts[j][1]-pts[j-1][1]
						ds=(dx**2+dy**2)**.5
						s2=s-n*pxpt
						if j<len(pts)-2 and s2>=pxpt:
							ticks.append((pts[j-1][0]+dx/ds*(s2-pxpt),pts[j-1][1]+dy/ds*(s2-pxpt)))
							n+=1
						s+=ds
						dp.append(s)
					for j in range(r):
						for n in range(len(ticks)):
							c=SpriteNode('Skin/sliderscorepoint.png',position=ticks[(-n-1 if j%2 else n)],scale=0,alpha=1)
							if self.mod_hd:
								#A.sequence(A.fade_to(.8,ar/2),
								c.run_action(A.group(A.sequence(A.wait(ar/2),A.fade_to(.5,ar/2),A.fade_to(.001,sdur*.75)),A.sequence(A.wait(ar+j*sdur/r+beatlen*(n-1)/2),A.scale_to(cs/128,.1)),A.sequence(A.wait(ar+j*sdur/r+beatlen*(n+1)-.1),A.fade_to(0,0))))
							else:
								c.run_action(A.group(A.sequence(A.wait(ar+j*sdur/r+beatlen*(n-1)/2),A.scale_to(cs/128,.1)),A.sequence(A.wait(ar+j*sdur/r+beatlen*(n+1)-.1),A.fade_to(0,0))))
							self.a.add_child(c)
					#print dp, l
					def pathf(node, progress):
						d=d1=progress*r
						d=d%1
						if int(d1)%2:
							d=1-d
						j=0
						while j<len(dp)-1 and dp[j]<l*d:
							j+=1
						j-=1
						k=(l*d-dp[j])/(dp[j+1]-dp[j])
						#print k
						#print (dp[j], l*d)
						dx=sd[i][0][j+1][0]-sd[i][0][j][0]
						dy=sd[i][0][j+1][1]-sd[i][0][j][1]
						#print dx, dy
						a,b=pts[j]
						node.position=(a+dx*k,b+dy*k)
					b.run_action(A.sequence(A.wait(ar),A.group(A.fade_to(1,.1),A.call(pathf,sdur)),A.fade_to(0,.1)))
					self.a.add_child(b)
			self.i+=1
		if self.leadin>0:
			self.leadin-=self.dt
		else:
			self.leadin=0
			
	def getbeat(self):
		t=self.player.current_time()
		tpt=self.tpts[self.tptn]
		pct=1-((t-tpt[3])%tpt[1])/tpt[1]
		return pct**2
			
	def touch_ended(self, touch):
		if len(self.touches)==1:
			if self.paused and self.player.current_time()>0:
				self.paused=False
				self.player.play()
			else:
				self.paused=True
				self.player.pause()
		if self.ts[0]-self.player.current_time()>3:
			self.player.seek(self.ts[0]-2)
			self.bg.run_action(A.sequence(A.wait(1.2),A.fade_to(self.bgdim,1)))
		
	def did_evaluate_actions(self):
		for node in self.a.children:
			if node.alpha==0:
				node.remove_from_parent()
		
	def playsong(self):
		self.player.play()
		#self.player.current_time()=200
	
	def stop(self):
		self.player.pause()
		self.stopped=True
		
	def load_sliders(self):
		k=self.si.keys()
		for i in k:
			if self.stopped:
				return
			sf=self.sliderfill if self.sliderfill else self.cols[self.otypes[i][1]]
			#print i
			self.si[i]=sliderlib.render_curve2(self.sd[i][0],self.cs,sf,self.slideredge)
			time.sleep(.01)

mods=0

#s=Osu('xi - FREEDOM DiVE (Nakagawa-Kanon) [FOUR DIMENSIONS].osu','FREEDOM DiVE',mods)
#s=Osu('xi - FREEDOM DiVE (Nakagawa-Kanon) [Another].osu','FREEDOM DiVE')
#s=Osu('Maffalda - pensamento tipico de esquerda caviar (Blue Dragon) [Gangsta].osu', '175036 pensamento tipico de esquerda caviar', mods)		
#s=Osu("Knife Party - Centipede (Sugoi-_-Desu) [This isn't a map, just a simple visualisation].osu",'150945 Centipede',mods)
s=Osu('UNDEAD CORPORATION - Everything will freeze (Ekoro) [Time Freeze].osu','158023 Everything will freeze',mods)
#s=Osu('Tatsh - IMAGE -MATERIAL- Version 0 (Scorpiour) [Scorpiour].osu','93523 IMAGE -MATERIAL- <Version 0>',mods)
#s=Osu('IOSYS - Endless Tewi-ma Park (Lanturn) [Tewi Spinners].osu','90935 Endless Tewi-ma Park')
#s=Osu('IOSYS - Endless Tewi-ma Park (Lanturn) [Tewi 2B Expert Edition].osu','90935 Endless Tewi-ma Park',mods)
#s=Osu('Tech N9ne - Worldwide Choppers (Blue Dragon) [Gangsta].osu', '137377 Worldwide Choppers',mods)
#s=Osu('LiSA - crossing field (TV Size) (CXu) [Insane].osu','crossing field (TV Size)')
#s=Osu('Halozy - Genryuu Kaiko (Hollow Wings) [Higan Torrent].osu','180138 Genryuu Kaiko',mods)
#s=Osu('DragonForce - Defenders (Spaghetti) [Legend].osu','323059 Defenders',mods)
#s=Osu('Function Phantom - Neuronecia (Amamiya Yuko) [Ethereal].osu','186911 Neuronecia',mods)
#s=Osu('DragonForce - Cry Thunder (Jenny) [Legend].osu','316050 Cry Thunder',mods)
#s=Osu('Panda Eyes & Teminite - Highscore (Fort) [Game Over].osu','332532 Highscore',mods)
#s=Osu("The Quick Brown Fox - The Big Black (Blue Dragon) [WHO'S AFRAID OF THE BIG BLACK].osu",'The Big Black',mods)
#s=Osu('yuikonnu - Otsukimi Recital (Mythol) [Collab].osu','107763 Otsukimi Recital',mods)
#s=Osu("Wakeshima Kanon - World's End, Girl's Rondo(Asterisk DnB Remix) (Meg) [We cry OPEN].osu","331499 World's End, Girl's Rondo(Asterisk DnB Remix)")
#s=Osu("Razihel & Virtual Riot - One For All, All For One (Fort) [Together We've Fallen].osu", '275655 One For All, All For One',mods)
#s=Osu('TK from Ling tosite sigure - unravel (TV edit) (xChippy) [Desperation].osu', '219107 unravel (TV edit)', mods)
#s=Osu('xi - Blue Zenith (Asphyxia) [FOUR DIMENSIONS].osu', '292301 Blue Zenith', mods)
#s=Osu("u's - Bokura no LIVE Kimi to no LIFE (Hinsvar) [Affection].osu", '189216 Bokura no LIVE Kimi to no LIFE', mods)
#s=Osu("u's - Kitto Seishun ga Kikoeru (Troll) [Youth].osu", '409073 Kitto Seishun ga Kikoeru', mods)
#s=Osu("gmtn. (witch's slave) - furioso melodia (Alumetorz) [Wrath].osu", '280107 furioso melodia', mods)

run(s,LANDSCAPE, show_fps=True)