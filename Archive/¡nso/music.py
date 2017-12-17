# coding: utf-8
from objc_util import *
from time import sleep
from datetime import datetime
import os
import sound

def search(path,ext='.mp3'):
	l=[]
	for i in os.listdir(path):
		p=os.path.join(path,i)
		if os.path.isdir(p):
			l.extend(search(p,ext))
		elif i[-len(ext):]==ext:
			l.append(p)
	return l

class Player (object):
	def __init__(self,path,rate=1):
		self.rate=rate
		AVAudioSession = ObjCClass('AVAudioSession')
		AVPlayer = ObjCClass('AVPlayer')
		AVPlayerItem = ObjCClass('AVPlayerItem')
		NSURL = ObjCClass('NSURL')
		#CMTime = ObjCClass('CMTime')
		
		audio_session = AVAudioSession.sharedInstance()
		audio_session.setCategory_withOptions_error_('AVAudioSessionCategoryPlayback', 1, None)

		sound = NSURL.fileURLWithPath_(path)
		item = AVPlayerItem.playerItemWithURL_(sound)

		self.player = AVPlayer.alloc().initWithPlayerItem_(item)
		self.player.setActionAtItemEnd_(2)
		
		self.duration=float(self.player.currentItem().asset().duration().a)/self.player.currentItem().asset().duration().b
		
	def play(self):
		self.player.play()
		self.player.setRate_(self.rate)
		
	def pause(self):
		self.player.pause()
		
	def current_time(self):
		return self.player.currentTime().a/1000000000.
		
	def setRate(self,rate):
		self.rate=rate
		self.player.setRate_(self.rate)
		
	def seek(self,t):
		s=self.player.currentTime()
		s.a=int(t*1000000000)
		self.player.seekToTime_(s)
	
	def seek_by(self,t):
		s=self.player.currentTime()
		s.a+=int(t*1000000000)
		self.player.seekToTime_(s)
		
for i in search('Songs'):
	p=Player(i)
#	p.play()
#	a=0
#	while 1:#p.current_time()<p.duration:
#		if p.current_time()>a:
#			print p.current_time()
#			a+=0.9230769230769231
		#sleep(1)
	break