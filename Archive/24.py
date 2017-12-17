from random import randint
from itertools import permutations
import re

r=1
l=False

def eq1(a,b):
	return abs(a-b)<.01

def filterp(eq):
	if '(' not in eq: return eq
	n=-1
	l=[]
	for i in range(len(eq)):
		if eq[i]=='(':
			l.append([i])
			n+=1
		if eq[i]==')':
			l[n].append(i)
			n-=1
	try:
		n=eval(eq)
	except:
		return eq
	temp=eq.replace('(','').replace(')','')
	try:
		if eq1(eval(temp),n):
			return temp
	except:pass
	if len(l)==2:
		if '((' not in eq and '))' not in eq:
			l[1].append(l[0].pop())
		for i in (0,1):
			temp=eq[:l[i][0]]+eq[l[i][0]+1:l[i][1]]+(eq[l[i][1]+1:] if l[i][1]<len(eq)-1 else '')
			try:
				if eq1(eval(temp),n):
					return temp
			except:pass
	return eq

while r:
	args=0
	s=raw_input().split()
	if len(s)>1: args=s[1:]
	if len(s): s=s[0]
	else: s=''
	print
	if s=='' or s=='new':
		l=[0,0,0,0]
		for i in range(4):
			n=randint(1,13)
			l[i]=n
			print n
		
	if (l or args) and s in ('s','solve'):
		if args:
			a,b,c,d=(int(i) for i in args)
		else:
			a,b,c,d=(str(i) for i in l)
		done=0
		found=set([])
		for a,b,c,d in permutations((a,b,c,d)):
			for o1 in ('+','-','*','/'):
				for o2 in ('+','-','*','/'):
					for o3 in ('+','-','*','/'):
						if '/' in (o1,o2,o3):
							a,b,c,d=(str(float(i)) for i in (a,b,c,d))
						else:
							a,b,c,d=(str(int(float(i))) for i in (a,b,c,d))
						for ans in (a+o1+b+o2+c+o3+d,a+o1+'('+b+o2+c+o3+d+')',a+o1+'('+b+o2+'('+c+o3+d+'))',a+o1+'(('+b+o2+c+')'+o3+d+')',a+o1+b+o2+'('+c+o3+d+')',a+o1+'('+b+o2+c+')'+o3+d,'('+a+o1+b+o2+c+')'+o3+d,'('+a+o1+'('+b+o2+c+'))'+o3+d,'(('+a+o1+b+')'+o2+c+')'+o3+d,'('+a+o1+b+')'+o2+c+o3+d,'('+a+o1+b+')'+o2+'('+c+o3+d+')'):
							ans=filterp(ans)
							if ans in found: continue
							try:
								if eq1(eval(ans),24):
									done=1
									found.add(ans)
									if '/' in (o1,o2,o3):
										def tempf(s):
											return str(int(float(s.group(0))))
										ans=re.sub('\d+.0',tempf,ans)
									print ans
									#break
							except: pass
						#if done: break
					#if done: break
				#if done: break
			#if done: break
		#else:
			#print 'No Solution'
		if not done: print 'No Solution'
		else: 
			n=len(found)
			print str(n)+(' solution found' if n==1 else ' solutions found')
		
	if s=='help':
		print 'help: help'
		print "new or '': next 4"
		print 's(olve) [a b c d]: solve current 4 or provide new 4 to solve'
		
	print
