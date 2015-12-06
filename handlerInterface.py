# coding: utf-8
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree

class HandlerInterface:

	def __init__(self, data):
		self.app_root=os.path.dirname(__file__)
		self.templates_root=os.path.join(self.app_root,'templates')
		self.render=web.template.render(self.templates_root)
		self.data=data

    #处理微信发送的订阅消息
	def onSubsribeMsg(self):
		xml=self.data
		fromUser=xml.find("FromUserName").text
		toUser=xml.find("ToUserName").text
		content=u'欢迎关注银宫微信公众账号,输入相应关键字可以获取信息:\n[1]银民'
		return self.render.reply_text(fromUser,toUser,int(time.time()),content)

	#处理微信发送普通文本消息
	def onPlainTextMsg(self):
		xml=self.data
		fromUser=xml.find("FromUserName").text
		toUser=xml.find("ToUserName").text
		content=xml.find("Content").text
		return self.render.reply_text(fromUser,toUser,int(time.time()),content)


