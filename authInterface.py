import urllib
import urllib2
import json

class AuthInterface:

	def __init__(self):
		self.appID='wxb753428e0ba72130'
		self.appSecret='a9bcb8fa690a27fe6931d495c279fff9'

	def getAccessToken(self):
		url='https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+appID+'&secret='+appSecret
		req=urllib2.Request(url)
		res=urllib2.urlopen(req)
		b_data=res.read()
		result=json.loads(bytes.decode(b_data))
		access_token=result['access_token']

		return access_token