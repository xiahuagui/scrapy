# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from tutorial.items import HuxiuItem
import pymysql.cursors


class HuxiuPipeline(object):
	def __init__(self):
		# 连接数据库
		connect = pymysql.Connect(
		    host='localhost',
		    port=3306,
		    user='dev',
		    passwd='1fi923^a3bui*9',
		    db='my_data',
		    charset='utf8'
		)
		# 获取游标
		cursor = connect.cursor()


    def process_item(self, item, spider):
    	print(item)
    	print(type(item))
        #return item
