import sae.const
import MySQLdb
import sys
import logging

MYSQL_DB=sae.const.MYSQL_DB
MYSQL_USER=sae.const.MYSQL_USER
MYSQL_PASS=sae.const.MYSQL_PASS
MYSQL_HOST=sae.const.MYSQL_HOST
MYSQL_PORT=sae.const.MYSQL_PORT
MYSQL_HOST_S=sae.const.MYSQL_HOST_S

class MySqlDaoInterface:

	def  __init__(self):
		self.conn=MySQLdb.connect(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASS,port=int(MYSQL_PORT),db=MYSQL_DB,charset='utf8')

	def testConn(self):
		cursor=self.conn.cursor()
		sql="select * from T_AG_GOSSIP"
		cursor.execute(sql)
		row=cursor.fetchone()
		print(row)