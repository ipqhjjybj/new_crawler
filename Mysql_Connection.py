#!/usr/bin/python
#coding: utf8

import os
import sys
import time
import string
import urllib2
import re
import json
import cymysql

from config import *
class MySQL(object):
	'''
	MYSQL 连接过程
	'''
	conn = ''
	cur = ''
	def __init__(self,host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWORD,db=MYSQL_DATABASE_NAME,charset=UTF_8_CHARSET):
		try:
			self.conn = cymysql.connect(host=host,user=user,passwd=passwd,db=db,charset=charset)
		except Exception,e:
			print e
			print Exception
			sys.exit()
		self.cur = self.conn.cursor()
		self.cur.execute("SET NAMES %s " % charset)
	#
	#	ret = a.sqlCondition()
	#
	def sqlCodition(self):
		return self.conn
	#
	#	a.runSql("select * from table")
	#
	def runSql(self , sql):
		self.cur.execute(sql)
	# 
	#   查询单个的结果
	#	a.getResult()
	#
	def getResult(self):
		return self.cur.fetchall()
	#
	#   插入数据到mysql
	#   a.insertData("qi",{"id":33,"name":"ah"})
	#
	def insertData(self, tablename , data):
		key = []
		val = []
		for i in range(len(data)):
			key.append(data.keys()[i])
			val.append("'"+str(data.values()[i])+"'")
		key1 = ",".join(key)
		val1 = ",".join(val)
		sql = "insert into " + tablename + "(" + key1 + ") values (" + val1 + ")"
		return sql
		
if __name__=="__main__":
	Stock.saveToStorage('2015-06-19')
