import sae.const
import MySQLdb
import sys
import logging

MYSQL_DB=sae.const.MYSQL_DB
MySQL_USER=sae.const.MySQL_USER
MYSQL_PASS=sae.const.MYSQL_PASS
MYSQL_HOST=sae.const.MYSQL_HOST
MYSQL_PORT=sae.const.MYSQL_PORT
MYSQL_HOST_S=sae.const.MYSQL_HOST_S

class MySqlDaoInterface:

	def  __init__(self):
		self.conn=MYSQLdb.connect(host=MYSQL_HOST,user=MySQL_USER,password=MYSQL_PASS,port=MYSQL_PORT,db=MYSQL_DB,charset='utf-8')

	def testConn(self):
		cursor=self.conn.cursor()
		sql="select * from T_AG_GOSSIP"
		cursor.execute(sql)
		row=cursor.fetchone()
		logging.error(row)
		print(row)