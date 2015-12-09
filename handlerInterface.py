# coding: utf-8
import web
import lxml
import time
import os
import logging
import urllib
import urllib2,json
import re
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
		u"[4].八卦|Gossip\n[5].田纳西|Tennessee Co.unLtd\n"+\
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
		print(re.search(r'天气$',str(content.encode('utf-8')))!=None)
		#获取欢迎消息
		if content=='0':
			return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),self.default_content)
		#获取银宫主页图文消息
		elif content=='1':
			return self.onAgPalace()
		#获取最新的八卦
		elif content=='4':
			return self.onGossip()
		#获取音乐推荐
		elif content=='music':
			return self.onMusic()
		#获取指定城市的天气
		elif re.search(r'天气$',str(content.encode('utf-8')))!=None:
			length=len(content)
			if(length==2):
				content="不加上城市名，你想我查哪个旮旯的天气?!"
				return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),content)
			key=content[0:length-2]
			key=key.encode('gb2312')
			return self.onWeather(key)
		elif content.encode('utf-8')=='翻译':
			return self.onTranslate(self)
		#测试数据库，开发用
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
			content=content+"["+str(gossip.time)+u"__"+gossip.title+u"]\n"+gossip.content+u"\n"
		return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),content)

	def onMusic(self):
		music_dao=MySqlDaoInterface()
		music=music_dao.getRandomMusic()
		#微信接口的模板是错的,而且需要使用带.mp3后缀的资源，使用起来不方便，暂时不用，改用图文推荐形式
		#print(self.render.reply_music(self.fromUser,self.toUser,int(time.time()),music.title,music.description,music.url))
		#return self.render.reply_music(self.fromUser,self.toUser,int(time.time()),music.title,music.description,music.url)
		return self.render.reply_pic_text(self.fromUser,self.toUser,int(time.time()),music.title,music.description,music.picurl,music.url)

	def onWeather(self,key):
		key=urllib.quote(key)

		url='http://php.weather.sina.com.cn/xml.php?city='+key+'&password=DJOYnieT8234jlsK&day=0'
		req=urllib2.Request(url)
		res=urllib2.urlopen(req)
		data=res.read()

		xml=etree.fromstring(data)
		if xml.find("Weather")!=None:	
			city=xml.find("Weather").find("city").text
			status1=xml.find("Weather").find("status1").text
			status2=xml.find("Weather").find("status2").text
			temperature1=xml.find("Weather").find("temperature1").text
			temperature2=xml.find("Weather").find("temperature2").text
			pollution=xml.find("Weather").find("pollution").text
			pollution_l=xml.find("Weather").find("pollution_l").text
			zwx_s=xml.find("Weather").find("zwx_s").text
			chy_shuoming=xml.find("Weather").find("chy_shuoming").text
			content=u'%s\n[%s/%s]\n温度:%s~%s°C-%s\n污染指数:%s-%s\n穿衣建议:%s'%(city,status2,status1,temperature2,temperature1,zwx_s,pollution,pollution_l,chy_shuoming)
			return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),content)
		else:
			content='尼玛，这是什么地方啊，我都查不到这旮旯的天气~'
			return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),content)
	
	#银宫/10班通讯录功能
	def onContact(self):
		return
	def onAdultVideo(self):
		return
	def onTranslate(self):
		url="http://fanyi.youdao.com/"
		return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),url)
	def testDB(self):
		test=MySqlDaoInterface()
		test.testConn()