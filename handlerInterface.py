# coding: utf-8
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree

class HandlerInterface:

	def __init__(self,data):
		self.app_root=os.path.dirname(__file__)
        self.templates_root=os.path.join(self.app_root,'templates')
        self.render=web.template.render(self.templates_root)
		self.data=data

    #处理微信发送的订阅消息
	def onSubsribeMsg(self):

	#处理微信发送的取消订阅消息
	def onUnsubsribeMsg(self):

	#处理微信发送普通文本消息
	def onPlainTextMsg(self):
		xml=self.data
		fromUser=xml.find("FromUserName").text
		toUser=xml.find("ToUserName").text
		content=xml.find("Content").text

		return self.render.reply_text(fromUser,toUser,int(time.time()),content)


