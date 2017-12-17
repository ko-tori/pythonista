from numbers import Number

funcs={}
funcs['+']=lambda a,b:a+b
funcs['-']=lambda a,b:a-b
funcs['*']=lambda a,b:a*b

oop={}
oop['+']=0
oop['-']=0
oop['*']=1
		
class Exp:
	def __init__(self, t, s, *args):
		self.t=t
		if t:
			self.fname=s
			self.f=funcs[s]
			self.args=args
		else:
			self.name=s
	
	def eval(self):
		if self.t:
			return self.f(*self.args)
		else:
			return self.name
	
	def __str__(self):
		ret=''
		i=0
		if self.t:
			for arg in self.args:
				if isinstance(arg, float):
					if int(arg)==arg:
						arg=int(arg)
					ret+=str(arg)
				elif arg.t and oop[arg.fname]<oop[self.fname]:
					ret+='('
					ret+=str(arg)
					ret+=')'
				else:
					ret+=str(arg)
				if isinstance(self.fname,str):
					if i<1:
						ret+=self.fname
				elif i<len(self.fname):
					ret+=self.fname[i]
				i+=1
			return ret
		else:
			return self.name
			
	def d(self):
		s='Expression(' if self.t else 'Symbol('
		if self.t:
			s+='%s, %s)'%(self.fname,str(self.args))
		else:
			s+=self.name
		return s
	
	def __add__(self, other):
		if isinstance(other,Number):
			other=float(other)
		return Exp(1,'+',self,other)
	
	def __radd__(self, other):
		if isinstance(other,Number):
			other=float(other)
		return Exp(1,'+',other,self)
		
	
			
def S(name):
	return Exp(0,name)
	
a=S('a')
exp=1+a+1
print exp
