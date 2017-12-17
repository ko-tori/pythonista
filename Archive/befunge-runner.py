from random import randint
from sys import stdout

prog='''
2>:3g" "-!v\  g30          <
 |!`"O":+1_:.:03p>03g+:"O"`|
 @               ^  p3\" ":<
2 234567890123456789012345678901234567890123456789012345678901234567890123456789
'''
grid=[list(i) for i in prog.split('\n') if i!='']
w=max(len(i) for i in grid)
h=len(grid)
grid=[i+[' ']*(w-len(i)) for i in grid]
stack=[]
loc=[0,0]
delta=2
for i in grid[0]:
	if i in '<^>v':
		delta=0 if i=='<' else 1 if i=='^' else 2 if i=='>' else 3 if i=='v' else 2
		break
	elif i!=' ':
		print 'warning: missing arrow!'
		loc=[0,0]
		break
	loc[0]+=1
strmode=False
output=''

def push(i):
	global stack
	stack.append(i)

def pop():
	global stack
	if len(stack)==0:
		raise Exception('stack popped nonexistent element')
	a=stack[-1]
	stack=stack[:-1]
	return a

while 1:
	c=grid[loc[1]][loc[0]]
	n=1
	if c=='"':
		strmode=not strmode
	elif strmode:
		push(ord(c))
	elif c in '0123456789':
		push(int(c))
	elif c=='@':
		break
	elif c=='#':
		n=2
	elif c=='<':
		delta=0
	elif c=='^':
		delta=1
	elif c=='>':
		delta=2
	elif c=='v':
		delta=3
	elif c=='?':
		delta=randint(0,3)
	elif c=='|':
		delta=3 if pop()==0 else 1
	elif c=='_':
		delta=2 if pop()==0 else 0
	elif c=='.':
		stdout.write(str(pop()))
	elif c==',':
		stdout.write(chr(pop()))
	elif c=='&':
		push(int(input()))
	elif c=='~':
		a=raw_input()
		if len(a)==1:
			push(ord(a))
	elif c=='$':
		pop()
	elif c=='\\':
		if len(stack)<2:
			push(0)
		else:
			a=pop()
			b=pop()
			push(a)
			push(b)
	elif c==':':
		if len(stack)==0:
			push(0)
		else:
			a=pop()
			push(a)
			push(a)
	elif c=='p':
		y=pop()
		x=pop()
		v=pop()
		grid[y][x]=chr(v)
	elif c=='g':
		y=pop()
		x=pop()
		if y>=h or x>=w:
			push(0)
		else:
			push(ord(str(grid[y][x])))
	elif c=='+':
		if not len(stack)<2:
			push(pop()+pop())
	elif c=='-':
		if not len(stack)<2:
			push(-pop()+pop())
	elif c=='*':
		if not len(stack)<2:
			push(pop()*pop())
	elif c=='/':
		if not len(stack)<2:
			a=pop()
			b=pop()
			if a==0:
				push(0)
			else:
				push(b/a)
	elif c=='%':
		if not len(stack)<2:
			a=pop()
			b=pop()
			if a==0:
				push(0)
			else:
				push(b/a)
	elif c=='!':
		push(1 if pop()==0 else 0)
	elif c=='`':
		a=pop()
		b=pop()
		push(1 if b>a else 0)
		
	if delta==0:
		loc[0]-=n
	if delta==1:
		loc[1]-=n
	if delta==2:
		loc[0]+=n
	if delta==3:
		loc[1]+=n
	loc[0]%=w
	loc[1]%=h

print '\n\ndone'
