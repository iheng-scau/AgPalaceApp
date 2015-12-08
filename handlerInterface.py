# coding: utf-8
import web
import lxml
import time
import os
import logging
import urllib2,json
from lxml import etree
#from authInterface import AuthInterface
#from mcDaoInterface import McDaoInterface
from mysqlDaoInterface import MySqlDaoInterface

class HandlerInterface:

	def __init__(self, data):
		self.app_root=os.path.dirname(__file__)
		self.templates_root=os.path.join(self.app_root,'templates')
		self.render=web.template.render(self.templates_root)
		self.data=data
		self.fromUser=data.find("FromUserName").text
		self.toUser=data.find("ToUserName").text
		self.default_content=u"欢迎关注银宫微信公众账号,输入相应关键字可以获取信息:\n"+\
		u"[1].银宫|Ag-Palace\n[2].银民|Ager\n[3].银学|Agadamic\n"+\
		u"[4].银闻|Ag-News\n[5].田纳西-Tennessee Co.unLtd\n"+\
		u"[6].活动|Agitivity\n[7].你懂的|Oh,shit!\n[8].关于/开发者|About/Developer\n"+\
		u"*回复相应的数字获取相关信息.\n"+\
		u"*回复0可再次获得本消息.\n"+\
		u"*Ag-Palace平台的功能还在不断完善中，如有意见或建议可联系我们:)"

    #处理微信发送的订阅消息
	def onSubsribeMsg(self):
		return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),self.default_content)

	#处理微信发送普通文本消息
	def onPlainTextMsg(self):
		xml=self.data
		content=xml.find("Content").text
		#获取欢迎消息
		if content=='0':
			return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),self.default_content)
		elif content=='1':
			return self.onAgPalace()
		elif content=='4':
			return self.onGossip()
		elif content=='music':
			test_content="<xml>+/<ToUserName><![CDATA["+self.fromUser+"]]></ToUserName><FromUserName><![CDATA["+self.toUser+"]]></FromUserName><CreateTime>$createTime</CreateTime><MsgType><![CDATA[music]]></MsgType><Music><Title><![CDATA[$title]]></Title><Description><![CDATA[$description]]></Description><MusicUrl><![CDATA[$music_url]]></MusicUrl><HQMusicUrl><![CDATA[HQ_MUSIC_Url]]></HQMusicUrl><ThumbMediaId><![CDATA[media_id]]></ThumbMediaId></Music></xml>"
			#return self.onMusic()
			return test_content
		elif content=='testdb':
			self.testDB()
		return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),content)

	#获取银宫信息
	def onAgPalace(self):
		logging.error(u'in')
		title='银宫 | Ag-Palace'
		description='Home Page of Ag-Palace'
		picurl='http://agpalaceapp.sinaapp.com/static/img/err.png'
		url='http://agpalaceapp.sinaapp.com/static/index.html'
		logging.error(self.render.reply_pic_text(self.fromUser,self.toUser,int(time.time()),title,description,picurl,url))
		return self.render.reply_pic_text(self.fromUser,self.toUser,int(time.time()),title,description,picurl,url)

	def onGossip(self):
		gossip_dao=MySqlDaoInterface()
		list=gossip_dao.getGossip()
		#logging.error("recieve "+str(len(list)))
		content=''
		for gossip in list:
			content=content+"["+gossip.title+u"-"+str(gossip.time)+u"]\n"+gossip.content+u"\n"
		return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),content)

	def onMusic(self):
		music_dao=MySqlDaoInterface()
		music=music_dao.getRandomMusic()
		print(self.render.reply_music(self.fromUser,self.toUser,int(time.time()),music.title,music.description,music.url))
		return self.render.reply_music(self.fromUser,self.toUser,int(time.time()),music.title,music.description,music.url)

	def testDB(self):
		test=MySqlDaoInterface()
		test.testConn()