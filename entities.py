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
	def __init__(self,title,url,description,picurl):
		self.title=title
		self.description=description
		self.url=url
		self.picurl=picurl
	def setTitle(self,title):
		self.title=title

	def setDescription(self,description):
		self.description=description

	def setUrl(self,url):
		self.url=url

	def setPicUrl(self,picurl):
		self.picurl=picurl
class Agitivity:
	def __init__(self,title,content,date,participant,note):
		self.title=title
		self.content=content
		self.participant=participant
		self.date=date
		self.note=note
class Ager:
	def __init__(self,name,description,img_url,wechat):
		self.name=name
		self.description=description
		self.img_url=img_url
		self.wechat=wechat
