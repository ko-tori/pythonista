import re

list1=['','one','two','three','four','five','six','seven','eight','nine']
list2=['','ten','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
list3=['ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
list4=['','thousand','million','billion','trillion','quadrillion','quintillion','sextillion','septillion','octillion','nonillion']
l1=['','un','duo','tre','quattuor','quin','se','septe','octo','nove']
l10=['','deci','viginti','triginta','quadraginta','quinquaginta','sexaginta','septuaginta','octoginta','nonaginta']
l100=['','centi','ducenti','trecenti','quadringenti','quingenti','sescenti','septingenti','octingenti','nongenti']
c1=[[],[],[],['s','x'],[],[],['s','x'],['m','n'],[],['m','n']]
c10=[[],['n'],['m','s'],['n','s'],['n','s'],['n','s'],['n'],['n'],['m','x'],[]]
c100=[[],['n','x'],['n'],['n','s'],['n','s'],['n','s'],['n'],['n'],['m','x'],[]]
vowels=['a','e','i','o','u']

def cw(n):
	n=(n-3)/3
	if n<10:
		return list4[n+1]
	

def wordify(n):
	if n==0: return 'zero'
	n=str(n)
	if n[0]=='-':
		negflag='negative '
		n=n[1:]
	else:
		negflag=''
	n=[int(i) for i in reversed(n)]
	r=''
	for i,j in enumerate(n):
		if i%3==0:
			if i>1 and len(n)-i<7 and (n[i+1] or n[i+2]):
					r=cw(i+1)+', '+r
		if i%3==0:
			if i<len(n)-1:
				if n[i+1]>1:
					r=list1[j]+' '+r
				if n[i+1]==0 and j!=0:
					r='and '+list1[j]+' '+r
			else:
				r=list1[j]+' '+r
		if i%3==1:
			if j==1:
				r=list3[n[i-1]]+' '+r
			elif n[i-1]==0 or j==0:
				r=list2[j]+r
			else:
				r=list2[j]+'-'+r
		if i%3==2:
			if j!=0:
				r=list1[j]+' hundred '+r
	return negflag+r
	
def commify(n):
	n=str(n)
	r=''
	if 0<len(n)%3<3: r=n[:len(n)%3]+','
	return (r+ ','.join(re.findall('...', n[::-1]))[::-1]).strip()

x=100000005795759
x=input()
print commify(x)
print wordify(x)