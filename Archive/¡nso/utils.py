import urllib as u,zipfile as z,urllib2 as u2
import time,os

def get_mapset(url):
	osz=u.urlretrieve(url, 'temp.osz')[0]
	f=z.ZipFile(osz,'r')
	p='Songs/temp'+str(time.clock())
	f.extractall(p)
	f.close()
	os.remove(osz)
	s=fix(p)
	for i in os.listdir(s):
		if i[-4:]=='.osu':
			print 'Osu(%s, %s, mods)' % (repr(i),repr(s[6:]))

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
	return 'Songs/'+i+t
	
def get_thing(url, loc):
	r=u2.urlopen(url)
	#f=open(loc,'w')
	#f.write(r.read())

def copy(file,dest):
	with open(file,'rb') as f:
		with open(dest,'w') as d:
			d.write(f.read())