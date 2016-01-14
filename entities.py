# coding:utf-8
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
class TrainInfo:
	#attrs
	train_code=''
	start_station=''
	end_station=''
	from_station=''
	to__station=''
	start_time=''
	arrive_time=''
	duration=''
	available=''
	#特等座
	sc_num='0'
	#一等座
	c1_num='0'
	#二等座
	c2_num='0'
	#软卧
	rw_num='0'
	#硬卧
	yw_num='0'
	#硬座
	yz_num='0'
	#无座
	wz_num='0'



