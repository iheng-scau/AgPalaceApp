import os
import sys

class Gossip:
	def __init__(self,title,content,time):
		self.title=title
		self.content=content
		self.time=time

	def setTitle(self,title):
		self.title=title

	def setContent(self,content):
		self.content=content

	def setTime(self,time):
		self.time=time

class Music:
	def __init__(self,title,url,descrption):
		self.title=title
		self.descrption=descrption
		self.url=url
	def setTitle(self,title):
		self.title=title

	def setDescription(self,descrption):
		self.descrption=descrption

	def setUrl(self,url):
		self.url=url
		