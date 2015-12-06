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

        def POST(self):
            str_xml=web.data()
            xml=etree.fromstring(str_xml)
            msgType=xml.find("MsgType").text
            fromUser=xml.find("FromUserName").text
            toUser=xml.find("ToUserName").text
            logging.error(u'-->[recieve msg]:from:'+fromUser+',msg type:'+msgType)

            handler=HandlerInterface(xml)
            result=':(-The message type is not supported by our Ag-Palace platform yet.'
            if msgType == 'text':
                result=handler.onPlainTextMsg()
            elif msgType == 'event':
                result=handler.onSubsribeMsg()
            else:
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"hello"+content)
            return result