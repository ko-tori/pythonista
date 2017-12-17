'''
To do:
Slider ticks/tick rate
Follow lines
Numbers?
'''

import sound,math,os,re,thread,time,urllib as u,zipfile as z
from scene import *
from PIL import Image,ImageOps as IOps
import sliderlib

def get_mapset(url):
	osz=u.urlretrieve(url, 'temp.osz')[0]
	f=z.ZipFile(osz,'r')
	p='Songs/temp'+str(time.clock())
	f.extractall(p)
	f.close()
	os.remove(osz)
	fix(p)
	
def fix(p):
	for f in os.listdir(p):
		if f[-4:]=='.osu':
			bm=[l.strip() for l in open(p+'/'+f,'r').readlines()]
			i=''
			for l in bm:
				if l[:6]=='Title:':
					t=l[6:]+''
				if l[:13]=='BeatmapSetID:':
					i=l[13:]+' '
	os.rename(p,'Songs/'+i+t)

def cs(n):
	return 88-8*(n-2)

def ar(n):
	return round(1.2-((n-5)*.15 if n>=5 else (n-5)*.12),4)
	
def pie(x,y,d,p):
	r=d/2
	cx,cy=x+r,y+r
	for i in range(45,int(p*180)+45):
		t=math.pi*i/180
		line(cx,cy,cx+r*math.cos(t*2),cy+r*math.sin(t*2))

class Osu(Scene):
	def __init__(self, song, folder, mods=0):
		self.song=song
		self.folder='Songs/'+folder
		self.mods=[mods&1,mods&2,mods&4,mods&8]
	
	def setup(self):
		self.hr=bool(self.mods[0])
		self.hd=bool(self.mods[2])
		self.bm=[l.strip() for l in open(self.folder+'/'+self.song,'r').readlines()]
		self.cols=[]
		for i,j in enumerate(self.bm):
			if j[:13]=='ApproachRate:':
				self.ar=ar(min(float(j[13:])*(1.4 if self.hr else 1),10))
			if j[:11]=='CircleSize:':
				self.cs=cs(float(j[11:])*(1.3 if self.hr else 1))
			if j[:15]=='AudioFilename: ':
				audiofile=self.folder+'/'+j[15:]
			if j[:14]=='StackLeniency:':
				stackl=float(j[14:])
			if j[:13]=='AudioLeadIn: ':
				self.leadin0=self.leadin=float(j[13:])/1000
			if j[:17]=='SliderMultiplier:':
				self.sliderx=sliderx=float(j[17:])
			r=re.sub('Combo\d : ','',j)
			if r!=j:
				self.cols.append(tuple(float(k)/255 for k in r.split(',')))
			if j=='//Background and Video events':
				bgpic=self.bm[i+1].split(',')[2][1:-1]
			if j=='[TimingPoints]':
				timingi=i+1
			if j=='[HitObjects]':
				break
		self.tpts=[]
		for l in self.bm[timingi:i]:
			if l=='[Colours]' or l=='':
				break
			stuff=[float(a) for a in l.split(',') if a]
			self.tpts.append((stuff[0]/1000.,stuff[1]/1000 if stuff[1]>0 else self.tpts[-1][1],-100./stuff[1] if stuff[1]<0 else 1,stuff[6]==1,stuff[7]==1))
		#tpts[n]=[time,beatlength,velocity,bpmchange,kiai]
		self.tptn=0
		self.objs=[i.split(',') for i in self.bm[i+1:]]
		self.ts=[int(i[2])/1000. for i in self.objs]
		self.x=[float(i[0]) for i in self.objs]
		self.y=[(float(i[1]) if self.hr else 384-float(i[1])) for i in self.objs]
		otypes=[(int(i[3])&11,int(i[3])&4) for i in self.objs]
		#Parse Object Types and Colors
		self.otypes=[]
		n=0
		for i,j in otypes:
			self.otypes.append((i,n))
			if j:
				n+=1
				n%=len(self.cols)
		self.ct=len(self.objs)
		#Stacking
		prev=self.x[0],self.y[0]
		tprev=self.ts[0]
		n=0
		stacks=[0]*self.ct
		for i in range(1,self.ct):
			if (self.x[i],self.y[i])==prev and self.ts[i]-tprev<stackl/4:
				n+=1
				stacks[i]=n
			else:
				n=0
			prev=self.x[i],self.y[i]
			tprev=self.ts[i]
		for i in range(self.ct):
			self.x[i]+=stacks[i]*2
			self.y[i]-=stacks[i]*2
		#Generate Slider Data
		si=[]
		self.sliderdata=[]
		n=0
		for i in range(self.ct):
			if self.otypes[i][0]==2:
				pts=self.objs[i][5].split('|')
				t=float(self.objs[i][2])/1000
				while n<len(self.tpts)-1 and self.tpts[n+1][0]<=t:
					n+=1
				st=pts[0]
				pts=[j.split(':') for j in pts[1:]]
				pts=[(self.x[i],self.y[i])]+[(int(j),(float(k) if self.hr else 384-float(k))) for j,k in pts]
				sd=[]
				if st in 'BL':
					
					sd.append(sliderlib.bezier(pts,float(self.objs[i][7])/3))
				elif st=='C':
					sd.append(sliderlib.catmullchain(pts,float(self.objs[i][7])/4))
				elif st=='P':
					sd.append(sliderlib.passthrough(pts,4))
				else:
					self.sliderdata.append(0)
				pxpb=sliderx*100*self.tpts[n][2]
				sbl=float(self.objs[i][6])*float(self.objs[i][7])/pxpb
				sd.append(sbl*self.tpts[n][1])
				sd.append(int(self.objs[i][6]))
				sd.append(n)
				self.sliderdata.append(sd)
				si.append(i)
				#sd[n]=[data,duration,timingpoint#,image=[identifier,x,y,w,h]]
			else:
				self.sliderdata.append(0)
		thread.start_new_thread(self.load_sliders,(si,))
		#time.sleep(1)
		try:
			self.bg=load_pil_image(IOps.fit(Image.open(self.folder+'/'+bgpic,).convert('RGBA'),(1024,748),Image.ANTIALIAS))
		except:
			self.bg=0
		self.circle=load_pil_image(Image.open('Skin/circle.png').convert('RGBA'))
		self.circleoverlay=load_pil_image(Image.open('Skin/circleoverlay.png').convert('RGBA'))
		self.approachcircle=load_pil_image(Image.open('Skin/approachcircle.png').convert('RGBA'))
		self.spinner=load_pil_image(Image.open('Skin/spinner.png').convert('RGBA'))
		self.spinner_as=load_pil_image(Image.open('Skin/Spinner-approachcircle.png').convert('RGBA'))
		self.rarrow=load_pil_image(Image.open('Skin/reversearrow.png').convert('RGBA'))
		self.start=thread.allocate_lock()
		self.start.acquire()
		thread.start_new_thread(self.test,(audiofile,))
		self.c=0
		self.ind=0
		self.ind2=0
		self.leadin*=-1
		self.playing=False
		self.frame_ct=0
		self.fps=60
		#self.start.release()
		time.sleep(0.2)
		
	def draw(self):
		if self.leadin<0:
			self.leadin+=self.dt
		self.frame_ct+=1
		i1,i2,pt,x,y,ts,ct,ots,sd,objs= self.ind,self.ind2,self.player.current_time+self.leadin,self.x,self.y,self.ts,self.ct,self.otypes,self.sliderdata,self.objs
		ar,cs=self.ar,float(self.cs)
		tpt=list(self.tpts[self.tptn])
		if tpt[3] and self.tptn>0:
			tpt[0]=self.tpts[self.tptn-1][0]
		background(0,0,0)
		if self.bg:
			tint(1,1,1,.2)#+.04*math.cos(tpt[0]+pt*math.pi/2/tpt[1]))
			image(self.bg,0,0)
		if ts[0]-pt>3 and self.playing:
			tint(1,1,1,.5+.2*math.cos(tpt[0]+pt*math.pi/2/tpt[1]))
			text('Skip >>>', 'Helvetica', 96, self.bounds.w-50, 50, 7)
		stroke(1,1,1)
		stroke_weight(1)
		pie(self.bounds.w-100,self.bounds.h-100,50,1-pt/self.player.duration)
		tint(1,1,1,.5)
		temp=render_text('{:-f}'.format(pt,3), 'Helvetica', 12)[1].w-10
		text('{:-f}'.format(pt,3), 'Helvetica', 12, self.bounds.w-temp, 20, 5)
		if not (self.frame_ct-1)%30: self.fps=1/self.dt
		text('fps: '+str(int(self.fps)), 'Helvetica', 12, 30, 20, 2)
		if not self.playing:
			if self.leadin>=-0.1:
				self.leadin=0
				self.playing=True
				try:
					self.start.release()
				except:pass
		#text(str(tpt[2]), 'Helvetica', 36, *self.bounds.center())
		#text(str(self.tptn)+':'+str(self.tpts[self.tptn]), 'Helvetica', 36, 256,192)
		push_matrix()
		scale(1.5,1.5)
		translate(*(i/1.5 for i in self.bounds.center()))
		translate(-256,-192)
		
		fadetime=.25
		
		k=ct
		for k in range(i1,ct): #k is how far rendering should go
			td=ts[k]-pt
			if sd[k] and len(sd[k])<6:
				sd[k].append(load_pil_image(sd[k][4][0]))
			if td>ar:
				break
				
		if 0:
			self.stop()
			run(Menu())
				
		for n in range(i2,k): #follow points?
			break
			if n>ct-2:
				break
			c=ots[n][1]
			if c!=ots[n+1][1] or ots[n+1][0]==8:
				continue
			td=ts[n]-pt
			td2=ts[n+1]-pt
			t=ots[n][0]
			a,b=x[n],y[n]
			alpha=1
			if t==2:
				td+=sd[n][1]
				if sd[n][2]%2:
					a,b=sd[n][0][-1][0],sd[n][0][-1][1]
			if td<=0:
				alpha=1+td2/fadetime
				f=1
			elif td<ar:
				f=1-td/ar
			else:
				continue
			a2,b2=x[n+1],y[n+1]
			d=((a-a2)**2+(b-b2)**2)**.5
			if d<cs:
				continue
			e=d/cs
			dx,dy=a2-a,b2-b
			fill(1,1,1,alpha)
			stroke_weight(0)
			#print d*alpha/e
			for i in range(int(d*f/e-.5)):
				ellipse(a+e*i/d*dx,b+e*i/d*dy,2,2)
				
		sbw=cs/24.
		if self.tptn<len(self.tpts)-1 and self.tpts[self.tptn+1][0]<=pt:
			self.tptn+=1
			
		for n in range(i2-1,k+1):
			if sd[n]:
				td=ts[n]-pt
				sdur=sd[n][1]
				if td>ar:
					continue
				if td>0:
					alpha=(1-td/ar,)
				else:
					alpha=(1+(td+sdur)/fadetime,)
				col=self.cols[ots[n][1]]
				fill(*col+alpha)
				tint(*col+alpha)
				stroke(1,1,1,*alpha)
				stroke_weight(sbw)
				#for a,b in sd[n][0]:
				#	ellipse(a-cs/2+sbw,b-cs/2+sbw,cs-2*sbw,cs-2*sbw)
				#stroke_weight(0)
				#for a,b in sd[n][0]:
				#	ellipse(a-cs/2+2*sbw,b-cs/2+2*sbw,cs-4*sbw,cs-4*sbw)
				tint(1,1,1,*alpha)
				image(sd[n][5],*sd[n][4][1:])
				a,b=sd[n][0][-1]
				if td>0:
					image(self.circleoverlay,sd[n][0][0][0]-cs/2,sd[n][0][0][1]-cs/2,cs,cs)
				image(self.circleoverlay,a-cs/2,b-cs/2,cs,cs)
				d,r,l=1,sd[n][2],len(sd[n][0])
				p=int(-td/sdur*r)
				if -sdur<=td<=0:
					ind=int(abs(td)/sdur*l*r)
					z=abs(td)/sdur*l*r-ind
					if ind%(2*l)==l:
						ind=l-1
					d=-1 if ind/l%2 else 1
					ind=ind%l*d
					if ind<0:
						ind-=1
					fill(1,1,1,.5)
					stroke(1,1,1,.6)
					stroke_weight(sbw*2)
					a,b=sd[n][0][ind]
					if -len(sd[n][0])<=ind+d<len(sd[n][0]):
						dx,dy=sd[n][0][ind+d][0]-a,sd[n][0][ind+d][1]-b
					else:
						dx=dy=0
					ellipse(a+dx*z-cs/2+sbw,b+dy*z-cs/2+sbw,cs-2*sbw,cs-2*sbw)
				if sd[n][2]-1:
					push_matrix()
					if p<r-1:
						a,b=sd[n][0][-1][0],sd[n][0][-1][1]
						t=math.degrees(math.atan2(sd[n][0][-2][1]-b,sd[n][0][-2][0]-a))
						translate(a,b)
						rotate(t)
						image(self.rarrow,-cs/3,-cs/3,2*cs/3,2*cs/3)
					pop_matrix()
					push_matrix()
					if td<0 and r>2 and p<r-2:
						a,b=sd[n][0][0][0],sd[n][0][0][1]
						t=math.degrees(math.atan2(sd[n][0][1][1]-b,sd[n][0][1][0]-a))
						translate(a,b)
						rotate(t)
						image(self.rarrow,-cs/3,-cs/3,2*cs/3,2*cs/3)
					pop_matrix()
			elif ots[n][0]==8:
				td=ts[n]-pt
				sdur=int(objs[n][5])/1000.-ts[n]
				if td>.25:
					continue
				if td>0:
					alpha=1-td/.25,
					h=384
				else:
					alpha=1,
					h=384*(1+td/sdur)
				tint(1,1,1,*alpha)
				pop_matrix()
				push_matrix()
				translate(*self.bounds.center())
				scale(1.5,1.5)
				fill(1,1,1,0)
				stroke(1,1,1,*alpha)
				stroke_weight(8*h/384)
				ellipse(-h/2,-h/2,h,h)
				#image(self.spinner_as,-h/2,-h/2,h,h)
				rotate((0 if td>0 else td)*1500)
				stroke_weight(2)
				#line(0,10,0,50)
				#image(self.spinner,-384/2,-384/2,384,384)
				pop_matrix()
				push_matrix()
				scale(1.5,1.5)
				translate(*(i/1.5 for i in self.bounds.center()))
				translate(-256,-192)
				
		for n in range(k-1,i1-1,-1): #fading in stuff
			td=ts[n]-pt
			hdoff=ar/2 if self.hd else 0
			if ots[n][0]==1	and td<=0.01+hdoff:
				self.ind+=1
			if ots[n][0]==2 and td<=.01:
					self.ind+=1
			if ots[n][0]==8 and float(objs[n][5])/1000-pt<=0.01:
					self.ind+=1
			if ots[n][0]<=2:
				alpha=(1-td/ar,)
				if not self.hd and td>0:
					tint(1,1,1,*alpha)
					d=(.5+1.3*td/ar)*cs
					image(self.approachcircle,x[n]-d,y[n]-d,2*d,2*d)
				if ots[n][0]==1:
					tint(*(self.cols[ots[n][1]]+alpha))
					image(self.circle,x[n]-cs/2,y[n]-cs/2,cs,cs)
					tint(1,1,1,*alpha)
					image(self.circleoverlay,x[n]-cs/2,y[n]-cs/2,cs,cs)
					
		for n in range(i1-1,i2-1,-1): #fading out stuff
			hdoff=ar/2 if self.hd else 0
			alpha=(1-(pt-ts[n]+hdoff)/fadetime,)
			dh=0 if self.hd else (1-alpha[0])*10
			tint(*(self.cols[ots[n][1]]+alpha))
			if ots[n][0]!=8:
				image(self.circle,x[n]-cs/2-dh,y[n]-cs/2-dh,cs+dh*2,cs+dh*2)
				tint(1,1,1,*alpha)
				image(self.circleoverlay,x[n]-cs/2-dh,y[n]-cs/2-dh,cs+dh*2,cs+dh*2)
				
		for i in range(i2,i1):
			if i<self.ct and pt-ts[i]>fadetime:
				if sd[i] and pt>fadetime+sd[i][1]+ts[i]:
					self.ind2+=1
					unload_image(sd[i][5])
				elif ots[i][0]==8 and int(objs[i][5])/1000.<pt:
					self.ind2+=1
				else:
					self.ind2+=1
				
		tint(1,1,1)
		#image(self.circle,256-cs/2,192-cs/2,cs,cs)
		#image(self.circleoverlay,256-cs/2,192-cs/2,cs,cs)
		pop_matrix()
		#rect(*tuple(self.bounds.center())+(2,2))
		fill(*(0,)*4)
		stroke(1,0,0)
		stroke_weight(2)
		#rect(92*1.5,57*1.5,512*1.5,384*1.5)

	def test(self, song):
		self.player=sound.Player(song)
		t=self.player.duration
		self.start.acquire()
		self.player.play()
		#self.player.current_time=60
		while self.player.current_time<t-.1 and self.playing:
			time.sleep(.1)
		self.player.stop()
		self.start.release()
		self.playing=False
	
	def stop(self):
		self.playing=False
	
	def touch_ended(self, touch):
		if self.ts[0]-self.player.current_time>3:
			self.player.current_time=self.ts[0]-2
			
	def load_sliders(self, si):
		sd=self.sliderdata
		for n in si:
			self.sliderdata[n].append(sliderlib.render_curve(sd[n][0],self.cs,self.cols[self.otypes[n][1]]))
			time.sleep(.1)

lmao=0
mods=1

#s=Osu('xi - FREEDOM DiVE (Nakagawa-Kanon) [FOUR DIMENSIONS].osu','FREEDOM DiVE')
#s=Osu('xi - FREEDOM DiVE (Nakagawa-Kanon) [Another].osu','FREEDOM DiVE')
#s=Osu('Maffalda - pensamento tipico de esquerda caviar (Blue Dragon) [Gangsta].osu', '175036 pensamento tipico de esquerda caviar', mods)		
#s=Osu("Knife Party - Centipede (Sugoi-_-Desu) [This isn't a map, just a simple visualisation].osu",'150945 Centipede',mods)
#s=Osu('UNDEAD CORPORATION - Everything will freeze (Ekoro) [Time Freeze].osu','158023 Everything will freeze',mods)
#s=Osu('Tatsh - IMAGE -MATERIAL- Version 0 (Scorpiour) [Scorpiour].osu','93523 IMAGE -MATERIAL- <Version 0>',mods)
#s=Osu('IOSYS - Endless Tewi-ma Park (Lanturn) [Tewi Spinners].osu','90935 Endless Tewi-ma Park')
#s=Osu('Tech N9ne - Worldwide Choppers (Blue Dragon) [Gangsta].osu', '137377 Worldwide Choppers',mods)
#s=Osu('LiSA - crossing field (TV Size) (CXu) [Insane].osu','crossing_field')
#s=Osu('Halozy - Genryuu Kaiko (Hollow Wings) [Higan Torrent].osu','180138 Genryuu Kaiko',mods)
#s=Osu('DragonForce - Defenders (Spaghetti) [Legend].osu','323059 Defenders',mods)
#s=Osu('Function Phantom - Neuronecia (Amamiya Yuko) [Ethereal].osu','186911 Neuronecia',mods)
#s=Osu('DragonForce - Cry Thunder (Jenny) [Legend].osu','316050 Cry Thunder',mods)
#s=Osu('Panda Eyes & Teminite - Highscore (Fort) [Game Over].osu','332532 Highscore',mods)
s=Osu("The Quick Brown Fox - The Big Black (Blue Dragon) [WHO'S AFRAID OF THE BIG BLACK].osu",'The Big Black',mods)

run(s,LANDSCAPE)

class Menu(Scene):
	def setup(self):
		pass
		
	def draw(self):
		background(0,0,0)
		tint(1,1,1)
		x,y=self.bounds.center()
		text('Tatsh - IMAGE -MATERIAL- Version 0', 'Helvetica', 16, x/2, y/2)
		text('UNDEAD CORPORATION - Everything will freeze', 'Helvetica', 16, 3*x/2, y/2)
		text('xi - FREEDOM DiVE', 'Helvetica', 16, x/2, 3*y/2)
		text('Knife Party - Centipede', 'Helvetica', 16, 3*x/2, 3*y/2)
		stroke_weight(5)
		stroke(1,1,1)
		line(x,0,x,self.bounds.h)
		line(0,y,self.bounds.w,y)
		
	def touch_ended(self, touch):
		if len(self.touches)>1:return
		x,y=self.bounds.center()
		a,b=touch.location
		if a>x:
			if b>y:
				self.s=Osu("Knife Party - Centipede (Sugoi-_-Desu) [This isn't a map, just a simple visualisation].osu",'centipede')
			else:
				self.s=Osu('UNDEAD CORPORATION - Everything will freeze (Ekoro) [Time Freeze].osu','freeze')
		else:
			if b>y:
				self.s=Osu('xi - FREEDOM DiVE (Nakagawa-Kanon) [FOUR DIMENSIONS].osu','fd')
			else:
				self.s=Osu('Tatsh - IMAGE -MATERIAL- Version 0 (Scorpiour) [Scorpiour].osu','imagemat')
		run(self.s,LANDSCAPE)

if lmao:
	m=Menu()
	run(m)
