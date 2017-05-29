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

from Mysql_Connection import *
class Stock:

	db_mysql_tushare = None

	#返回正常化的股票代码
	@staticmethod
	def norm_code(code):
		code = str(code)
		l = 6 - len(code)
		return '0' * l + code
	#判断是否是合格的股票代码
	@staticmethod
	def is_code(code):
		code = Stock.norm_code(code)
		if len(code) != 6:
			return False
		if code[:2] == "60" or code[:2] == "00" or code[:2] == "30":
			return True
		return False
	#判断交易市场
	@staticmethod
	def get_market(code):
		code = Stock.norm_code(code)
		if len(code) == 6:
			if code[:2] == "60":
				return "sh"
			if code[:2] == "00" or code[:2] == "30":
				return "sz"
		return "unknown"

	#返回对应字符串的 数据库
	@staticmethod
	def getDB(db_name):
		ret = None
		if db_name == 'mysql_tushare':
			if Stock.db_mysql_tushare == None:
				Stock.db_mysql_tushare = MySQL(host=MYSQL_HOST,user=MYSQL_USER,passwd=MYSQL_PASSWORD,db=DATABASE_NAME,charset=UTF_8_CHARSET)
			ret = Stock.db_mysql_tushare
		return ret

	#将tushre数据导入到 mysql中， 覆盖掉原先有的
	# Stock.downloadStockDataFromTushare('600848.SH',)
	# autype in ['hfq' , 'qfq']
	@staticmethod
	def downloadStockDataFromTushare(stock_code, start_time , end_time , autype , override = True):
		qt_autype = None
		table_name = ""
		if autype == "hfq":
			table_name = "rhq_hfq"
			qt_autype = 'hfq'
		if autype == 'qfq':
			table_name = 'rhq_qfq'
			qt_autype = None
		# delete 
		if override == True:
			
