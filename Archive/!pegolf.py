import itertools
from itertools import *
import math
import fractions
from operator import mul

def one():
	return sum(i for i in range(1000)if not(i%5 and i%3))
	
def two():
	r=.5+5**.5/2;sum(n for n in[int((r**n-(-r)**-n)/5**.5)for n in range(34)]if n%2-1)
	
def two2():
	r=.5+5**.5/2;f=lambda x:int((r**x-(-r)**-x)/5**.5);sum(f(n)for n in range(34)if f(n)%2-1)
	
def two3():
	return sum([n for n in[int(((.5+5**.5/2)**n-(-.5-5**.5/2)**-n)/5**.5)for n in range(34)]if n%2-1])
	
def three():
	return max(i for i in range(9,6**5)if 600851475143%i==0)

def four():
	print max(i[0]*i[1]for i in combinations(range(100,1000),2)if str(i[0]*i[1])==str(i[0]*i[1])[::-1])
	
def five():
	l=lambda a,b:a*b/fractions.gcd(a,b);reduce(l,range(7,20))

def six():
	return 5050**2-sum(i**2 for i in range(101))
	
def seven():
	N=7**6;sorted(reduce((lambda r,x:r-set(range(x**2,N,x))if(x in r)else r),range(2,N),set(range(2,N))))[10000]
	
def nine(): #120 chars
	a=[(a,b)for a,b in itertools.combinations(range(3,500),2)if(a**2+b**2)**.5+a+b==1000][0];a[0]*a[1]*(a[0]**2+a[1]**2)**.5
	
def nine2(): #132 chars
	p=lambda a,b:(a**2+b**2)**.5;a=[(a,b)for a,b in itertools.combinations(range(3,500),2)if a+b+p(a,b)==1000][0];a[0]*a[1]*p(a[0],a[1])
	
def nine3(): #131 chars
	p=lambda a,b:(a**2+b**2)**.5;a=[(a,b,p(a,b))for a,b in itertools.combinations(range(3,500),2)if a+b+p(a,b)==1000][0];a[0]*a[1]*a[2]
	
def thirtyfour():
	return sum(i for i in range(3,1000000)if sum(math.factorial(int(x))for x in str(i))==i)
	
def primes(N): #primes up to N
	return reduce((lambda r,x:r-set(range(x**2,N,x))if(x in r)else r),range(2,N),set(range(2,N)))

