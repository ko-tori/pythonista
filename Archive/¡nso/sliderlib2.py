from math import factorial as fa,atan2,sin,cos,pi
import ui,cStringIO
from PIL import Image

def bcoef(n,k):
	return fa(n)/fa(k)/fa(n-k)

def spline_len(p):
	return sum(((p[i][0]-p[i+1][0])**2+(p[i][1]-p[i+1][1])**2)**.5 for i in range(len(p)-1))
	
def lenp(p):
	n=len(p)-1
	if len(p)==2:
		return ((p[1][0]-p[0][0])**2+(p[1][1]-p[0][1])**2)**.5
	px,py=p[0]
	l=0
	for i in range(101):
			t=i/100.
			x,y=(sum(((bcoef(n,i)*(1-t)**(n-i)*t**i*p[i][j]) for i in range(n+1))) for j in (0,1))
			l+=((x-px)**2+(y-py)**2)**.5
			px,py=x,y
	return l
	
def bezier2(p,l=''):
	if l=='':
		l=lenp(p)
	prec=l/25.
	n=len(p)-1
	def b(t): 
		return (sum(((bcoef(n,i)*(1-t)**(n-i)*t**i*p[i][j]) for i in range(n+1))) for j in (0,1))
	arr=[]
	l1=0
	prevx,prevy=p[0]
	for i in range(int(l/prec)):
		t=i*prec/l
		#print t, i*prec/l
		x,y=b(t)
		dx,dy=x-prevx,y-prevy
		m=((dx)**2+(dy)**2)**.5
		#if m==0:print p
		if m!=0 and l1+m>=l:
			return arr+[(prevx+dx/m*(l1-l),prevy+dy/m*(l1-l))],l
		arr.append((x,y))
		l1+=m
		prevx,prevy=x,y
	return arr,l1
		

def line(p, l=-1, step=10.):
	dx,dy=p[1][0]-p[0][0],p[1][1]-p[0][1]
	m=(dx**2+dy**2)**.5/step
	if l==-1:
		l=m*step
	dx,dy=dx/m,dy/m
	a=[(p[0][0]+dx*i,p[0][1]+dy*i) for i in range(int(l/step+.5))]
	return a+[(p[0][0]+dx*l/step,p[0][1]+dy*l/step)],l

def bezier(p, l):
	if len(p)==2:
		return line(p,l)[0]
	arr=[]
	prev=0
	for i in range(1,len(p)+1):
		if i==len(p):
			part=p[prev:i]
			if len(part)==2:
				c=line(part,l)
			else:
				c=bezier2(part,l)
			arr+=c[0]
			#print l
		elif i<len(p) and p[i]==p[i-1]:
			part=p[prev:i]
			#print part
			if len(part)==2:
				c=line(part)
			else:
				c=bezier2(part)
			arr+=c[0][:-1]
			l-=c[1]
			prev=i
	if not arr:
		arr=bezier2(p)
	return arr

def passthrough(p,l,step=8.):
	a,b,c=(tuple(float(i) for i in j) for j in p)
	x1,y1,x2,y2=((i+j)/2. for i,j in zip(a+b,b+c))
	if a[1]==b[1]==c[1]:
		return line(p,l)[0]
	if a[1]==b[1]:
		m=-(b[0]-c[0])/(b[1]-c[1])
		x=x1
		y=m*(x-x2)+y2
	elif b[1]==c[1]:
		m=-(b[0]-a[0])/(b[1]-a[1])
		x=x2
		y=m*(x-x1)+y1
	else:
		m1,m2=(-(k-i)/(l-j) for i,j,k,l in ((a+b),(b+c)))
		if m1==m2:
			return line(p,l)[0]
		x=(m1*x1-m2*x2-y1+y2)/(m1-m2)
		y=m1*(x-x1)+y1
	r=((x-a[0])**2+(y-a[1])**2)**.5
	print m1,m2,x1,y1,x2,y2
	t=l/r
	d=(-1 if ((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))<0 else 1)
	t1=atan2(a[1]-y,a[0]-x)
	dt=step*t/l
	p=[]
	for i in range(int(t/dt)):
		i*=d
		p.append((x+r*cos(t1+dt*i),y+r*sin(t1+dt*i)))
	p.append((x+r*cos(t1+t*d),y+r*sin(t1+t*d)))
	return p
	
def render_curve(p, cs=72., c=(0,0,0), c2=(1,1,1)):
	cs*=34/36.
	x,y=zip(*p)
	minx,miny=min(x),min(y)
	maxx,maxy=max(x),max(y)
	w,h=maxx-minx,maxy-miny
	y=[h-i for i in y]
	sbw=cs/30.
	with ui.ImageContext(w+cs,h+cs) as ctx:
		ui.set_color(c2)
		for a,b in zip(x,y):
			o=ui.Path.oval(a+1.5*sbw-minx,miny+b+1.5*sbw,cs-3*sbw,cs-3*sbw)
			o.line_width=2*sbw
			o.stroke()
		ui.set_color(c)
		for a,b in zip(x,y):
			o2=ui.Path.oval(a+2*sbw-minx,miny+b+2*sbw,cs-4*sbw,cs-4*sbw)
			o2.line_width=0
			o2.fill()
		ui.set_color((0,0,1))
		img=ctx.get_image()
		return img, (minx-cs/2, -min(y)-cs/2)

def render_curve2(p, cs=72., c1=(0,0,0), c2=(1,1,1)):
	k=1.
	cs*=11/12.
	x,y=zip(*p)
	minx,miny=min(x),min(y)
	maxx,maxy=max(x),max(y)
	w,h=maxx-minx,maxy-miny
	y=[h-i for i in y]
	with ui.ImageContext(w+cs,h+cs) as ctx:
		a=0
		o=ui.Path()
		o.line_cap_style=1
		o.line_join_style=1
		o.move_to(x[0]-minx+cs/2,y[0]+miny+cs/2)
		for i in range(1,len(p)):
			o.line_to(x[i]-minx+cs/2,y[i]+miny+cs/2)
		#o.line_to(x[-1]-minx+cs/2,y[-1]+miny+cs/2)
		while a<cs/k:
			break
			o.line_width=cs-a*k
			if a==0:
				ui.set_color(c2)
				a+=cs/10/k
			else:
				c=(a/cs*k/4)
				ui.set_color(tuple(v1+v2 for v1,v2 in zip(c1,(c,c,c))))
				a+=k
			o.stroke()
		img=ctx.get_image()
		return img, (minx-cs/2, -min(y)-cs/2)

#Catmulls are deprecated

def catmull(p,n,z):
	n=float(n)/z
	def tj(ti, i, j):
		xi,yi=i
		xj,yj=j
		return (((xj-xi)**2+(yj-yi)**2)**0.5)**a+ti
	t0 = 0
	t1 = tj(t0, p[0], p[1])
	t2 = tj(t1, p[1], p[2])
	t3 = tj(t2, p[2], p[3])
	c=[[],[]]
	for i in range(int(n)+1):
		t=t1+i/n*(t2-t1)
		for xy in (0,1):
			a1=(t1-t)/(t1-t0)*p[0][xy]+(t-t0)/(t1-t0)*p[1][xy]
			a2=(t2-t)/(t2-t1)*p[1][xy]+(t-t1)/(t2-t1)*p[2][xy]
			a3=(t3-t)/(t3-t2)*p[2][xy]+(t-t2)/(t3-t2)*p[3][xy]
			b1=(t2-t)/(t2-t0)*a1+(t-t0)/(t2-t0)*a2
			b2=(t3-t)/(t3-t1)*a2+(t-t1)/(t3-t1)*a3
			c[xy].append((t2-t)/(t2-t1)*b1+(t-t1)/(t2-t1)*b2)
	return zip(*c)

def catmullchain(p,n):
	c=[]
	l=len(p)-3
	for i in range(l):
		c.extend(catmull([p[i],p[i+1],p[i+2],p[i+3]],n/l if l>1 else n))
	return c
