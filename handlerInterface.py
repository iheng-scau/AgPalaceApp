# coding: utf-8
import web
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
from entities import TrainInfo

class HandlerInterface:

	def __init__(self, data):
		self.app_root=os.path.dirname(__file__)
		self.templates_root=os.path.join(self.app_root,'templates')
		self.render=web.template.render(self.templates_root)
		self.data=data
		self.fromUser=data.find("FromUserName").text
		self.toUser=data.find("ToUserName").text
		self.default_content=\
		u"欢迎关注银宫微信公众账号,输入相应关键字可以获取信息:\n"+\
		u"[1].银宫|Ag-Palace\n[2].银民|Ager\n[3].银学|Agadamic\n"+\
		u"[4].八卦|Gossip\n[5].田纳西|Tennessee Co.unLtd\n"+\
		u"[6].活动|Agitivity\n[7].你懂的|Oh,shit!\n[8].关于/开发者|About/Developer\n"+\
		u"[i].更多的指令说明请回复 i 查看使用说明|Instructions\n"+\
		u"*回复相应的数字获取相关信息.所有包含的功能未全部列出,隐藏功能等你发现,你懂的~\n"+\
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
		#获取银宫主页图文消息
		elif content=='1':
			return self.onAgPalace()
		elif content=='2':
			return self.onAger()
		elif content=='3':
			return self.onAgadamic()
		#获取最新的八卦
		elif content=='4':
			return self.onGossip()
		#田纳西消息
		elif content=='5':
			return self.onTennessee()
		#银宫活动
		elif content=='6':
			return self.onAgitivity()
		#小福利推送
		elif content=='7':
			return self.onBonus()
		#关于
		elif content=='8':
			return self.onAbout()
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
		#进行火车票查询
		elif re.search(r'^火车',str(content.encode('utf-8')))!=None:
			length=len(content)
			key_array=content.split("\\")
			t_train_code=key_array[1]
			date=key_array[2]
			city=key_array[3]
			print city+'k'
			mode=key_array[4]
			print t_train_code+date
			result_str=self.onTrainInfo(t_train_code,date,city,mode)
			return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),result_str)
		#翻译功能(Deprecated)
		elif content.encode('utf-8')=='翻译':
			return self.onTranslate()
		#获取使用说明
		elif content=='i':
			title=u'银宫微信公众号使用说明'
			content=u'除了主菜单列出的功能之外，本公众号还不定时新增一些辅助的小功能供各位银民使用,\
			并且已有的小功能和新功能都在进行不定期的更新和上线。\n'+\
			u'[music]，发送 music 获取音乐推荐，由于微信音乐消息存在bug，暂时使用图文消息进行推荐。\n'+\
			u'[天气]，输入城市+天气可以查询城市明天的天气，如 广州天气\n'+\
			u'[翻译]，翻译现在已经下线，但是保留功能识别，系统会默认推荐有道\n'+\
			u'[火车信息]，输入格式 火车/车次/时间/城市/往返 如发送 火车/G1002/2016-02-14/深圳/L 可查询G1002次列车的开往韶关的信息,最后一个字母R表示去往韶关，L表示离开韶关(12306网站不稳定可能导致查询失败)'+'\n'+\
			u'[隐藏功能]，发送某些关键字可发现隐藏的功能，在此不具体列出\n'+\
			u'*暂时开放的功能可能存在缺陷或者不响应(SAE有可能发生延迟)，如果您对小功能有什么想法，欢迎联系我们:iheng_scau@hotmail.com'
			return self.render.reply_pic_text(self.fromUser,self.toUser,int(time.time()),title,content,'','')
			
		#测试数据库，开发用
		elif content=='testdb':
			self.testDB()

	#获取银宫信息
	def onAgPalace(self):
		logging.error(u'in')
		title='银宫 | Ag-Palace'
		description='银宫主页 | 银宫是由银皇立班一世所创立，并有多位资深银民组成的银性组织，旨在进行银学研究与交流以及论理性与感性的高雅学术活动。并且我们从不生产八卦，我们只是八卦的搬运工。\n(c)2008-2015,Ag-Palace'
		picurl='http://agpalaceapp.sinaapp.com/static/img/agp-clogo.jpg'
		url='http://agpalaceapp.sinaapp.com/static/index.html'
		logging.error(self.render.reply_pic_text(self.fromUser,self.toUser,int(time.time()),title,description,picurl,url))
		return self.render.reply_pic_text(self.fromUser,self.toUser,int(time.time()),title,description,picurl,url)
	
	#获取银民
	def onAger(self):
		ager_dao=MySqlDaoInterface()
		ager=ager_dao.getAgerInfo()
		return self.render.reply_pic_text(self.fromUser,self.toUser,int(time.time()),ager.name,ager.description,ager.img_url,'')

	#田纳西
	def onTennessee(self):
		content=u'田纳西Women Co.unLtd的相关的Play功能和田纳西湿词库还在建设中,敬请期待...'
		return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),content)

	#银学
	def onAgadamic(self):
		content=u'银学这么勃大茎深的学术，仅限内部交流，暂不开放'
		return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),content)

	#获取八卦
	def onGossip(self):
		gossip_dao=MySqlDaoInterface()
		list=gossip_dao.getGossip()
		#logging.error("recieve "+str(len(list)))
		content=''
		for gossip in list:
			content=content+"["+str(gossip.time)+u"__"+gossip.title+u"]\n"+gossip.content+u"\n"
		return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),content)

	#关于
	def onAbout(self):
		content=u'银宫公众平台是基于Python开发的微信公众平台并且已经在Github上面作为开源项目,现部署在新浪云(SAE),存储使用MySQL和Memcache(log:2016-01-13已禁用memcache服务)的方式.\n'+\
		u'-----------------\n项目信息:\n开发者: iheng-scau\n平台版本: 0.1\nPython: 2.7.x\n上线时间: 2015-12-03\n最近更新时间:2016-01-14\nGithub主页: https://github.com/iheng-scau/AgPalaceApp(点击详情访问)'
		return self.render.reply_pic_text(self.fromUser,self.toUser,int(time.time()),'关于银宫公众平台/开发者',content,'','')

	#音乐推荐功能
	def onMusic(self):
		music_dao=MySqlDaoInterface()
		music=music_dao.getRandomMusic()
		#微信接口的模板是错的,而且需要使用带.mp3后缀的资源，使用起来不方便，暂时不用，改用图文推荐形式
		#print(self.render.reply_music(self.fromUser,self.toUser,int(time.time()),music.title,music.description,music.url))
		#return self.render.reply_music(self.fromUser,self.toUser,int(time.time()),music.title,music.description,music.url)
		return self.render.reply_pic_text(self.fromUser,self.toUser,int(time.time()),music.title,music.description,music.picurl,music.url)

	#天气查询功能
	def onWeather(self,key):
		key=urllib.quote(key)

		url='http://php.weather.sina.com.cn/xml.php?city='+key+'&password=DJOYnieT8234jlsK&day=1'
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
			content=u'%s-明天天气情况\n[%s/%s]\n温度:%s~%s°C-%s\n污染指数:%s-%s\n穿衣建议:%s'%(city,status2,status1,temperature2,temperature1,zwx_s,pollution,pollution_l,chy_shuoming)
			return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),content)
		else:
			content='尼玛，这是什么地方啊，我都查不到这旮旯的天气~'
			return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),content)

	#获取银宫活动
	def onAgitivity(self):
		agitivity_dao=MySqlDaoInterface()
		agitivity=agitivity_dao.getLastAgitivity()
		content=u"[银宫活动公告牌]\n%s-活动时间:%s\n活动描述:%s\n备注:%s\n-----------------\n回复 +1 即可参加该活动哦~"%(agitivity.title,agitivity.date,agitivity.content,agitivity.note)
		return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),content)

	#福利推送
	def onBonus(self):
		list=[u"-家庭教师の亂ガヴァネス.avi",u"-制服フェティシズム.avi",u"-可爱いメイド爆乳.rmvb",u"PS:资源推送为限定功能，只有通过申请才使用本功能。赶紧点开链接吧~"]
		title=u'番号/百度云/磁力链接/torrent'
		content='\n'.join(list)
		picurl=u'http://agpalaceapp.sinaapp.com/static/img/fbiwarning.png'
		return self.render.reply_pic_text(self.fromUser,self.toUser,int(time.time()),title,content,picurl,u'http://www.shdf.gov.cn/')

	#银宫/10班通讯录功能
	def onContact(self):
		return
	#推荐小电影功能
	def onAdultVideo(self):
		return
	#翻译功能
	def onTranslate(self):
		url="虽然本大人的英语很好,应付你这水平的翻译,去问有道就够了:\nhttp://fanyi.youdao.com/"
		return self.render.reply_text(self.fromUser,self.toUser,int(time.time()),url)
	#如果发送的文本不在功能列表中，则使用自动回复功能
	def onAutoReply(self):
		return
	#火车信息查询
	def onTrainInfo(self,t_train_code,date,city,mode):
		train_code_dict={u'广州':'GZQ',u'上海':'SHH',u'韶关':'SNQ',u'深圳':'SZQ',u'太原':'TYV'}
		if mode=='R':
			from_station=train_code_dict.get(city)
			to_station=train_code_dict.get(u'韶关')
		else:
			from_station=train_code_dict.get(u'韶关')
			to_station=train_code_dict.get(city)

		url=str(self.render.train_site_url(date,from_station,to_station))
		print url
		req=urllib2.Request(url)
		res=urllib2.urlopen(req)
		json_data=res.read()
		print len(json_data)
		data=json.loads(json_data)
		result=TrainInfo()
		for index in range(len(data['data'])):
			train_code=data['data'][index]['queryLeftNewDTO']['station_train_code']
			if train_code==t_train_code:
				result.train_code=data['data'][index]['queryLeftNewDTO']['station_train_code']
				result.start_station=data['data'][index]['queryLeftNewDTO']['start_station_name']
				result.end_station=data['data'][index]['queryLeftNewDTO']['end_station_name']
				result.from_station=data['data'][index]['queryLeftNewDTO']['from_station_name']
				result.to__station=data['data'][index]['queryLeftNewDTO']['to_station_name']
				result.start_time=data['data'][index]['queryLeftNewDTO']['start_time']
				result.arrive_time=data['data'][index]['queryLeftNewDTO']['arrive_time']
				result.duration=data['data'][index]['queryLeftNewDTO']['lishiValue']
				result.available=data['data'][index]['queryLeftNewDTO']['canWebBuy']
				result.sw_num=data['data'][index]['queryLeftNewDTO']['swz_num']
				result.sc_num=data['data'][index]['queryLeftNewDTO']['tz_num']
				result.c1_num=data['data'][index]['queryLeftNewDTO']['zy_num']
				result.c2_num=data['data'][index]['queryLeftNewDTO']['ze_num']
				result.rw_num=data['data'][index]['queryLeftNewDTO']['rw_num']
				result.yw_num=data['data'][index]['queryLeftNewDTO']['yw_num']
				result.yz_num=data['data'][index]['queryLeftNewDTO']['yz_num']
				result.wz_num=data['data'][index]['queryLeftNewDTO']['wz_num']

		result_str=result.train_code+'_'+result.start_station+'-'+result.end_station+'\n'+\
			result.from_station+u'发车:'+result.start_time+'-'+result.to__station+u'到达:'+result.arrive_time+'('+result.duration+'min)'+'\n'+\
			u'是否有余票(Y/N):'+result.available+'\n'+\
			u'[商务/特等/一等/二等]:'+result.sw_num+'/'+result.sc_num+'/'+result.c1_num+'/'+result.c2_num+'\n'+\
			u'[软卧/硬卧/硬座/无座]:'+result.yw_num+'/'+result.yw_num+'/'+result.yz_num+'/'+result.wz_num
		return result_str

	#测试数据库
	def testDB(self):
		test=MySqlDaoInterface()
		test.testConn()