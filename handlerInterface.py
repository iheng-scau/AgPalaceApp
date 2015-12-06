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
		self.default_content=u'''欢迎关注银宫微信公众账号,输入相应关键字可以获取信息:
		[1].银宫-Ag-Palace\n[2].银民-Ager\n[3].银学-Agadamic
		[4].银闻-Ag-News\n[5].田纳西-Tennessee Women Co.unLtd
		[6].活动-Agitivity\n[7].你懂的-Oh,shit!\n[8].关于/开发者-About/Developer\n
		*回复相应的数字获取相关信息.
		*回复\'0\'可再次获得本消息.
		*Ag-Palace平台的功能还在不断完善中，如有意见或建议可联系我们:)'''

    #处理微信发送的订阅消息
	def onSubsribeMsg(self):
		xml=self.data
		fromUser=xml.find("FromUserName").text
		toUser=xml.find("ToUserName").text
		return self.render.reply_text(fromUser,toUser,int(time.time()),self.default_content)

	#处理微信发送普通文本消息
	def onPlainTextMsg(self):
		xml=self.data
		fromUser=xml.find("FromUserName").text
		toUser=xml.find("ToUserName").text
		content=xml.find("Content").text
		if content=='0':
			return self.render.reply_text(fromUser,toUser,int(time.time()),self.default_content)
		return self.render.reply_text(fromUser,toUser,int(time.time()),content)


