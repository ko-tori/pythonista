# coding: utf-8
import ui
import Image
import thread
import photos
from console import hud_alert
from random import random
import cStringIO

DEBUG=False

root='placeholder'
paths=[]
ccolor=(1,0,0,1)
cweight=5
cmode=0
bg=(1,1,1)
touchct=0
maxpath=5
base=False

def colorchooser_c(sender):
	v = sender.superview
	try:
		v['view1'].background_color = (v['r'].value, v['g'].value, v['b'].value, v['a'].value)
	except:
		v['view1'].background_color = (v['r'].value, v['g'].value, v['b'].value)
	
def colorchooser_shuffle(sender):
	v = sender.superview
	v['r'].value=random()
	v['g'].value=random()
	v['b'].value=random()
	colorchooser_c(sender)
	
def colorchooser_ok(sender):
	u=sender.superview
	global ccolor
	r=(u['r'].value,u['g'].value,u['b'].value)
	if not u['a'] is None:
		r+=(u['a'].value,)
	ccolor=r
	root['sidebar']['color'].background_color=ccolor
	sender.superview.close()

def color(sender):
	global ccolor
	col=tuple([float(i) for i in ccolor])
	u=ui.load_view('colorchooser')
	r,g,b=u['r'],u['g'],u['b']
	r.value,g.value,b.value=col[0:3]
	if len(col)==4:
		a=u['a']
		a.value=col[3]
	else:
		u.remove_subview(u['a'])
		u.height-=42
	colorchooser_c(r)
	u.present('sheet')
	while u.on_screen:
		pass
	sender.background_color=ccolor

def pick(a):
	global base
	temp=photos.pick_image()
	if not temp is None:
		base=render(temp, 726, 589)
		root['canvas'].rebase()
		refresh()
		hud_alert('Loaded')
	
def render(temp, w, h):
	r=temp.size
	if r[0]>r[1]:
		r=(w, w*r[1]/r[0])
	else:
		r=(h*r[0]/r[1], h)
	temp=temp.resize(r)
	strio=cStringIO.StringIO()
	temp.save(strio, 'PNG')
	return ui.Image.from_data(strio.getvalue())

def load(sender):
	global base
	clear()
	try:
		thread.start_new_thread(pick, (1,))
	except:
		pass
	
def brush(sender):
	global cweight
	cweight=(sender.value+.01)*25
	
def undo(sender):
	global paths
	paths=paths[:-1]
	refresh()
	
def mode(sender):
	global cmode
	if sender.name=='curve':
		cmode=0
	if sender.name=='cfill':
		cmode=1
	sender.font=('<system-bold>', sender.font[1])
	for i in sender.superview.subviews:
		if i!= sender:
			i.font=('<system>', sender.font[1])
	
def clear(sender=None):
	global paths, base
	base=False
	paths=[]
	if not sender is None:
		sender.superview.superview['canvas'].set_needs_display()

def getpic(canvas, arg=False):
	with ui.ImageContext(*canvas.bounds[2:4]) as ctx:
		temp=paths[:-maxpath] if arg else paths	
		if base:
			base.draw()
		else:
			ui.set_color(bg)
			ui.fill_rect(0,0,*canvas.bounds[2:4])
		for s,c,m in temp:
			ui.set_color(c)
			if m==0:
				s.stroke()
			if m==1:
				s.fill()
		return ctx.get_image()
		
def save(sender):
	if photos.save_image(getpic(sender.superview.superview['canvas'])):
		sender.title='Saved'
		hud_alert('Saved')
	else:
		sender.title='Error'
		pass
		
def refresh():
	root['canvas'].set_needs_display()

class Draw (ui.View):
	def __init__(self):
		self.multitouch_enabled=False
	
	def draw(self):
		global base,paths,touchct,maxpath
		if DEBUG:
			self.superview['debug'].text=str(len(paths))
		if base:
			base.draw()
		else:
			ui.set_color(bg)
			ui.fill_rect(0,0,*self.bounds[2:4])
		for s,c,m in paths:
			ui.set_color(c)
			if m==0:
				s.stroke()
			if m==1:
				s.fill()
		if touchct==0 and len(paths)>=maxpath:
			self.rebase(True)

	def touch_began(self, touch):
		#global ccolor
		#ccolor=(random(),random(),random(),1)
		global touchct
		touchct+=1
		p=ui.Path()
		p.line_cap_style=1
		p.line_join_style=1
		p.line_width=cweight
		paths.append((p,ccolor,cmode))
		paths[-1][0].move_to(*touch.location)

	def touch_moved(self, touch):
		paths[-1][0].line_to(*touch.location)
		self.set_needs_display()
		self.superview['sidebar']['save'].title='Save'
		
	def touch_ended(self, touch):
		global touchct,maxpath
		touchct-=1
		self.set_needs_display()
	
	def rebase(self, arg=False):
		global paths, base
		base=getpic(self, arg)
		if len(paths)>1:
			paths=paths[-maxpath:] if arg else paths[-1]
		
root=ui.load_view('Draw')
if not DEBUG:
	root.remove_subview(root['debug'])
root.present(orientations=('landscape', 'landscape-upside-down'))
