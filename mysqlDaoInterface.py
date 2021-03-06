#encoding=utf-8
import sae.const
import MySQLdb
import sys
import logging
import random
from entities import Gossip
from entities import Music
from entities import Agitivity
from entities import Ager


MYSQL_DB=sae.const.MYSQL_DB
MYSQL_USER=sae.const.MYSQL_USER
MYSQL_PASS=sae.const.MYSQL_PASS
MYSQL_HOST=sae.const.MYSQL_HOST
MYSQL_PORT=sae.const.MYSQL_PORT
MYSQL_HOST_S=sae.const.MYSQL_HOST_S

#针对mysql的dao
class MySqlDaoInterface:

	def  __init__(self):
		self.conn=MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASS,port=int(MYSQL_PORT),db=MYSQL_DB,charset='utf8')

	def testConn(self):
		cursor=self.conn.cursor()
		sql="select * from T_AG_GOSSIP"
		cursor.execute(sql)
		row=cursor.fetchone()
		print(row[1])

	def getGossip(self):
		cursor=self.conn.cursor()
		sql="select title,content,time from T_AG_GOSSIP g order by g.time desc limit 5"
		cursor.execute(sql)
		rows=cursor.fetchall()
		list=[]
		for row in rows:
			title=row[0]
			content=row[1]
			time=row[2]
			gossip=Gossip(title,content,time)
			list.append(gossip)
		self.conn.close()
		logging.error("return "+str(len(list))+" item")
		return list

	def getGossipBykey(self,key):
		cursor=self.conn.cursor()
		sql="select title,content,time from T_AG_GOSSIP g where g.key like \'%"+key+"%\' order by g.time desc limit 5 "
		cursor.execute(sql)
		rows=cursor.fetchall()
		list=[]
		for row in rows:
			title=row[0]
			content=row[1]
			time=row[2]
			gossip=Gossip(title,content,time)
			list.apend(gossip)
		self.conn.close()
		return list

	def getRandomMusic(self):
		cursor=self.conn.cursor()
		sql="select count(*) from T_AG_MUSIC"
		cursor.execute(sql)
		row=cursor.fetchone()
		music_num=row[0]
		random_num=random.randint(0,music_num-1)

		sql="select title,url,description,picurl from T_AG_MUSIC limit "+str(random_num)+",1"
		cursor.execute(sql)
		row=cursor.fetchone()

		music=Music(row[0],row[1],row[2],row[3])
		self.conn.close()
		return music

	def getLastAgitivity(self):
		cursor=self.conn.cursor()
		sql="select title,content,date,participants,notes from T_AG_AGITIVITY a order by a.date desc limit 0,1"
		cursor.execute(sql)
		row=cursor.fetchone()
		agitivity=Agitivity(row[0],row[1],row[2],row[3],row[4])
		return agitivity

	def getAgerInfo(self):
		cursor=self.conn.cursor()
		sql=u"select name,description,img_url,wechat from T_AG_AGER a where a.name='李伟健'"
		cursor.execute(sql)
		row=cursor.fetchone()
		ager=Ager(row[0],row[1],row[2],row[3])
		return ager
