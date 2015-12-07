import pylibmc as mencache
import os

class McDaoInterface:

	def __init__(self):
		self.mc=mencache.Client()
		
	def setVlue(self,key,value):
		return self.mc.set(key,value)

	def getValue(self,key):
		return self.mc.get(key)
		
