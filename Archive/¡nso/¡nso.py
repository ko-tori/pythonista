#coding: utf-8

'''
To do:

BROKEN: REBUILD -> ¡nso v2
	
Mods
Slider ticks/tick rate
Follow lines
Numbers?
Input
Linear sliders don't alway go far enough?
'''

import sound,math,os,re,thread,time
from scene import *
from PIL import Image,ImageOps as IOps
import sliderlib

def cs(n):
	return 88-8*(n-2)

def ar(n):
	return round(1.2-((n-5)*.15 if n>=5 else (n-5)*.12),4)
	
def od(n):
	return .0795-.006*n,.1395-.008*n,.1995-.01*n

def sinterp(n):
	return -math.cos(math.pi*n)/2+.5
	
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
		self.auto=1#False
		self.hr=bool(self.mods[0])
		self.hd=bool(self.mods[2])
		self.ez=bool(self.mods[1])
		self.bm=[l.strip() for l in open(self.folder+'/'+self.song,'r').readlines()]
		self.cols=[]
		for i,j in enumerate(self.bm):
			if j[:13]=='ApproachRate:':
				self.ar=ar(min(float(j[13:])*(1.4 if self.hr else 1),10)/(2 if self.ez else 1))
			if j[:18]=='OverallDifficulty:':
				self.odw=od(min(float(j[18:])*(1.4 if self.hr else 1),10))
			if j[:11]=='CircleSize:':
				self.cs=cs(float(j[11:])*(1.3 if self.hr else 1)/(2 if self.ez else 1))
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
		self.hitdata=[[-1,0]] #[hit time, hit type] hit types: 0: not hit yet, 1: 300, 2: 100, 3: 50, 4: miss
		self.objs=[i.split(',') for i in self.bm[i+1:]]
		self.ts=[int(i[2])/1000. for i in self.objs]
		self.x=[float(i[0]) for i in self.objs]
		self.y=[(float(i[1]) if self.hr else 384-float(i[1])) for i in self.objs]
		otypes=[(int(i[3])&11,int(i[3])&4) for i in self.objs]
		
		#self.cols=[(0,0,0)]
		
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
			self.x[i]+=stacks[i]*self.cs/24
			self.y[i]-=stacks[i]*self.cs/24
		#Cursor trail
		self.trail=[]
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
				l=float(self.objs[i][7])
				if st in 'BL':
					temp=[]
					i0=0
					for j in range(1,len(pts)):
						if pts[j]==pts[j-1] or j==len(pts)-1:
							lp=sliderlib.spline_len(sliderlib.bezier(pts[i0:j+1],3,100,''))
							if lp==0:
								break
							temp+=sliderlib.bezier(pts[i0:j+1],3,lp,l)
							i0=j
							l-=lp
					sd.append(temp)
				elif st=='C':
					sd.append(sliderlib.catmullchain(pts,l,4))
				elif st=='P':
					sd.append(sliderlib.passthrough(pts,l))
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
		self.slideredge=(1,1,1)
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
		self.pauseb=load_pil_image(Image.open('Skin/pausebutton.png').convert('RGBA'))
		self.cursor=load_pil_image(Image.open('Skin/cursor.png').convert('RGBA'))
		#self.cursortrail=load_pil_image(Image.open('Skin/cursortrail.png').convert('RGBA'))
		self.cursortrail=load_pil_image(Image.open('Skin/cursortrail2.png').convert('RGBA'))
		#self.cursortrail=None
		self.start=thread.allocate_lock()
		self.start.acquire()
		thread.start_new_thread(self.test,(audiofile,))
		self.c=0
		self.ind=0
		self.ind2=0
		self.cur=0
		self.leadin*=-1
		self.playing=False
		self.frame_ct=0
		self.fps=60
		self.btn=0
		self.btnv=0
		self.cursorsize=30
		self.inputloc=list(self.bounds.center())
		self.inputloc[1]-=1000
		self.paused=False
		self.bump=0
		self.beatb=0
		self.t1=0
		s=215./27
		sr=self.spinnerr=64
		#s=2.
		self.spinnerf=(lambda n:256-sr*math.sin(2*math.pi*s*n),lambda n:192+sr*math.cos(2*math.pi*s*n))
		#self.start.release()
		time.sleep(0.2)
		
	def draw(self):
		if self.leadin<0:
			self.leadin+=self.dt
		i1,i2,pt,x,y,ts,ct,ots,sd,objs=self.ind,self.ind2,self.player.current_time+self.leadin,self.x,self.y,self.ts,self.ct,self.otypes,self.sliderdata,self.objs
		ar,cs,od=self.ar,float(self.cs),self.odw
		tpt=list(self.tpts[self.tptn])
		if tpt[3] and self.tptn>0:
			tpt[0]=self.tpts[self.tptn-1][0]
		self.beatb=1-((pt-tpt[0])%tpt[1])/tpt[1]
		background(0,0,0)
		if self.bg:
			tint(1,1,1,.15)#+.05*self.beatb)
			image(self.bg,*self.bounds)
		if ts[0]-pt>3 and self.playing:
			tint(1,1,1,.5-.2*math.cos(math.pi/2/tpt[1]*(pt-tpt[0])))
			text('Skip >>>', 'Helvetica', 96, self.bounds.w-50, 50, 7)
		stroke(1,1,1)
		stroke_weight(1)
		pie(self.bounds.w-75,self.bounds.h-160,50,1-pt/ts[-1])
		tint(1,1,1)
		image(self.pauseb,self.bounds.w-85,self.bounds.h-105, 75, 75)
		tint(1,1,1,.5)
		text('{:-f}'.format(pt,3), 'Helvetica', 12, 30, 20, 2)
		if not self.playing:
			if self.leadin>=-0.1:
				self.leadin=0
				self.playing=True
				try:
					self.start.release()
				except:pass
		#text(str(self.beatb), 'Helvetica', 36, *self.bounds.center())
		#rect(0,10,20+self.beatb*20,20+self.beatb*20)
		#text(str((tpt[1]*(pt-tpt[0]))%tpt[1]), 'Helvetica', 36, 256,192)
		push_matrix()
		scale(1.5,1.5)
		translate(*(i/1.5 for i in self.bounds.center()))
		translate(-256,-192)
		
		fadetime=.25
		curx=cury=0
		
		k=ct
		for k in range(i1,ct): #k is how far rendering should go
			td=ts[k]-pt
			if td>ar:
				break
			if sd[k] and len(sd[k])<6:
				sd[k].append(load_pil_image(sd[k][4][0]))
				
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
		if self.tptn<len(self.tpts)-1 and self.tpts[self.tptn+1][0]<=pt:#timing point number
			self.tptn+=1
			
		for n in range(i2-1,k+1): #drawing sliders and spinners
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
				a1,b1=sd[n][0][-1]
				if td>0:
					image(self.circleoverlay,sd[n][0][0][0]-cs/2,sd[n][0][0][1]-cs/2,cs,cs)
				d,r,l=1,sd[n][2],len(sd[n][0])
				p=int(-td/sdur*r)
				if -sdur<=td<=0:
					ind=int(abs(td)/sdur*l*r)
					z=abs(td)/sdur*l*r-ind
					if ind%(2*l)==l:
						ind=l-1
					d=-1 if ind/l%2 else 1
					ind=ind%l*d
					if abs(ind)<2:
						self.bump=1
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
					curx,cury=a+dx*z,b+dy*z
				#text(str(p), 'Helvetica', 36, *self.bounds.center())
				if p<=r-1 or -td>sdur:
					image(self.circleoverlay,a1-cs/2,b1-cs/2,cs,cs)
				if r-1:
					push_matrix()
					if p<r-1:
						a,b=sd[n][0][-1][0],sd[n][0][-1][1]
						t=math.degrees(math.atan2(sd[n][0][-2][1]-b,sd[n][0][-2][0]-a))
						translate(a,b)
						rotate(t)
						ds=self.beatb*5
						image(self.rarrow,-cs/3-ds/2,-cs/3-ds/2,2*cs/3+ds,2*cs/3+ds)
					pop_matrix()
					push_matrix()
					if td<0 and r>2 and p<r-2:
						a,b=sd[n][0][0][0],sd[n][0][0][1]
						t=math.degrees(math.atan2(sd[n][0][1][1]-b,sd[n][0][1][0]-a))
						translate(a,b)
						rotate(t)
						image(self.circleoverlay,-cs/2,-cs/2,cs,cs)
						ds=self.beatb*10
						image(self.rarrow,-cs/3-ds/2,-cs/3-ds/2,2*cs/3+ds,2*cs/3+ds)
					pop_matrix()
			elif ots[n][0]==8:
				td=ts[n]-pt
				sdur=int(objs[n][5])/1000.-ts[n]
				if td>ar:
					continue
				if td>0:
					alpha=1-td/ar,
					h=384
				else:
					alpha=1,
					h=384*(1+td/sdur)
					if not -td>sdur:
						f1,f2=self.spinnerf
						curx,cury=f1(td),f2(td)
						#self.paused=True
						#self.player.pause()
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
			if (ots[n][0]==1	and td<=0.01+hdoff) or (ots[n][0]==2 and td<=0) or (ots[n][0]==8 and float(objs[n][5])/1000-pt<=0.01):
				self.ind+=1
				self.bump=1
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
		
		while 1:
			if self.cur<ct and pt-ts[self.cur]>=od[2]:
				self.cur+=1
			else:
				break
		
		if 0:
			tr=self.trail
			for i in range(len(tr)):
				a=float(i)/len(tr)
				tint(a,0,0,a)
				j=tr[i]
				trs=(a)**.5*self.cursorsize*3/4
				image(self.cursortrail,j[0]-trs/2,j[1]-trs/2,trs,trs)
		elif 1:
			tr=self.trail
			for i in range(len(tr)-1):
				a=float(i)/len(tr)
				stroke(a,0,0,a)
				fill(a,0,0,a)
				j=tr[i]+tr[i+1]
				r=a**.5*self.cursorsize/4+self.bump*6
				stroke_weight(r)
				line(*j)
				stroke_weight(0)
				ellipse(j[0]-r/2,j[1]-r/2,r,r)
		
		tint(1,1,1)
		curs=self.cursorsize+self.btnv*self.cursorsize/2
		if self.auto:
			i=self.ind
			if i==0:
				prevx,prevy=256,192
			else:
				if ots[i-1][0]==2:
					prevx,prevy=sd[i-1][0][-(sd[i-1][2]%2)]
				elif ots[i-1][0]==8:
					td=ts[i-1]-int(objs[i-1][5])/1000.
					f1,f2=self.spinnerf
					prevx,prevy=f1(td),f2(td)
				else:
					prevx,prevy=x[i-1],y[i-1]
			if ots[i][0]==8:
				dx,dy=256-prevx,192+self.spinnerr-prevy
			else:
				dx,dy=x[i]-prevx,y[i]-prevy
			p=0.
			if i>0:
				p=ts[i-1]
				if ots[i-1][0]==2:
					p+=sd[i-1][1]
				if ots[i-1][0]==8:
					p+=int(objs[i-1][5])/1000.-ts[i-1]
			pt=min(max(pt,0),ts[-1])
			temp=ts[i]-p
			p=1 if temp==0 else (pt-p)/temp
			p=sinterp(p)
			if curx==cury==0:
				curx,cury=prevx+dx*p,prevy+dy*p
			image(self.cursor,curx-curs/2,cury-curs/2,curs,curs)
		else:
			if self.t1:
				self.inputloc=list(self.touches[self.t1].location)
			c0,c1=self.bounds.center()
			curx,cury=(self.inputloc[0]-c0)/1.5+256,(self.inputloc[1]-c1)/1.5+192
			image(self.cursor,curx-curs/2,cury-curs/2,curs,curs)
		if not self.paused:
			self.trail.append((curx,cury))
			self.trail=self.trail[-10:]
		
		#image(self.circle,256-cs/2,192-cs/2,cs,cs)
		#image(self.circleoverlay,256-cs/2,192-cs/2,cs,cs)
		pop_matrix()
		#rect(*tuple(self.bounds.center())+(2,2))
		fill(*(0,)*4)
		stroke(1,0,0)
		stroke_weight(2)
		#boundbox
		#rect(92*1.5,57*1.5,512*1.5,384*1.5)
		#text('%d, %d' % (self.n, self.ind),'Helvetica',36,*self.bounds.center())
		self.btnv=max(min(self.btnv+(.2 if self.btn else -.2),1),0)
		r=self.bounds
		d=50+self.btnv*8
		fill(1,0,0)
		stroke_weight(0)
		rect(r.w-d,r.h/2-d/2,d,d)
		if not self.paused:
			self.bump=max(0,self.bump-.05)
	
	def touch_began(self, touch):
		if not touch.location in Rect(self.bounds.w-85,self.bounds.h-105, 75, 75):
			self.btn=1
			self.btnv=0
			if len(self.touches)==1:
				self.t1=touch.touch_id	
	
	def touch_ended(self, touch):
		if touch.touch_id==self.t1:
			if len(self.touches)==0:
				self.t1=0
			else:
				self.t1=self.touches.values()[0].touch_id
		if touch.location in Rect(self.bounds.w-85,self.bounds.h-105, 75, 75):
			if self.paused:
				self.player.play()
			else:
				self.player.pause()
			self.paused=not self.paused
		elif self.ts[0]-self.player.current_time>3:
			self.player.current_time=self.ts[0]-2
		if len(self.touches)==0:
			self.btn=0

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
		self.stopped=True
		self.playing=False
		try:
			unload_image(self.circle)
			unload_image(self.circleoverlay)
			unload_image(self.approachcircle)
			unload_image(self.spinner)
			unload_image(self.spinner_as)
			unload_image(self.rarrow)
			unload_image(self.pauseb)
			unload_image(self.cursor)
			unload_image(self.cursortrail)
			for i in self.sliderdata:
				if i:
					if len(i)>5:
						unload_image(i[5])
					else:
						break
			unload_image(self.bg)
		except:
			pass
			
	def load_sliders(self, si):
		self.n=0
		self.si=si
		sd=self.sliderdata
		self.stopped=False
		for n in si:
			if self.stopped:
				thread.exit()
			self.n=n
			self.sliderdata[n].append(sliderlib.render_curve(sd[n][0],self.cs,self.cols[self.otypes[n][1]],self.slideredge))
			time.sleep(.1)
			
import gc
gc.collect()

lmao=0
mods=0

#s=Osu('xi - FREEDOM DiVE (Nakagawa-Kanon) [FOUR DIMENSIONS].osu','FREEDOM DiVE',mods)
#s=Osu('xi - FREEDOM DiVE (Nakagawa-Kanon) [Another].osu','FREEDOM DiVE')
#s=Osu('Maffalda - pensamento tipico de esquerda caviar (Blue Dragon) [Gangsta].osu', '175036 pensamento tipico de esquerda caviar', mods)		
#s=Osu("Knife Party - Centipede (Sugoi-_-Desu) [This isn't a map, just a simple visualisation].osu",'150945 Centipede',mods)
#s=Osu('UNDEAD CORPORATION - Everything will freeze (Ekoro) [Time Freeze].osu','158023 Everything will freeze',mods)
s=Osu('Tatsh - IMAGE -MATERIAL- Version 0 (Scorpiour) [Scorpiour].osu','93523 IMAGE -MATERIAL- <Version 0>',mods)
#s=Osu('IOSYS - Endless Tewi-ma Park (Lanturn) [Tewi Spinners].osu','90935 Endless Tewi-ma Park')
#s=Osu('IOSYS - Endless Tewi-ma Park (Lanturn) [Tewi 2B Expert Edition].osu','90935 Endless Tewi-ma Park')
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

run(s,LANDSCAPE, show_fps=True)

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