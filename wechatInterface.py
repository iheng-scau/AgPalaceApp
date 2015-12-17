# coding: utf-8
import hashlib
import web
import lxml
import time
import os
import logging
import urllib2,json
from lxml import etree
from handlerInterface import HandlerInterface

class WechatInterface:
        def __init__(self):
            self.app_root=os.path.dirname(__file__)
            self.templates_root=os.path.join(self.app_root,'templates')
            self.render=web.template.render(self.templates_root)

        #微信平台验证token的时候会发送GET请求，由本方法进行处理
        #只要是GET请求都会进入本方法进行处理，但是本方法只针对微信平台发来的信息进行处理
        #如果是别的GET请求会导致本方法报错
        def GET(self):
            data=web.input()
            signature=data.signature
            timestamp=data.timestamp
            nonce=data.nonce
            echostr=data.echostr

            token="agpalaceapp"

            list=[token,timestamp,nonce]
            list.sort()
            sha1=hashlib.sha1()
            map(sha1.update,list)
            hashcode=sha1.hexdigest()
            if hashcode == signature:
                return echostr

        #由微信发送过来的消息是以POST方法请求的，由POST方法进行处理
        def POST(self):
            str_xml=web.data()
            xml=etree.fromstring(str_xml)
            msgType=xml.find("MsgType").text
            fromUser=xml.find("FromUserName").text
            toUser=xml.find("ToUserName").text
            logging.error(u'-->[recieve msg]:from:'+fromUser+',msg type:'+msgType)

            handler=HandlerInterface(xml)
            result=':(-The message type is not supported by our Ag-Palace platform yet.'
            #处理普通文本消息入口
            if msgType == 'text':
                result=handler.onPlainTextMsg()
            #处理时间消息入口
            elif msgType == 'event':
                result=handler.onSubsribeMsg()
            #如果不是普通文本或时间消息
            else:
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"hello"+content)
            return result