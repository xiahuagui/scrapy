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
		self.connect = pymysql.Connect(
		    host='localhost',
		    port=3306,
		    user='dev',
		    passwd='1fi923^a3bui*9',
		    db='my_data',
		    charset='utf8'
		)
		# 获取游标
		self.cursor = connect.cursor()


    def process_item(self, item, spider):
    	data = (item["title"].encode("utf-8"),item["url"].encode("utf-8"),item["pic"].encode("utf-8"))
    	sql = "INSERT INTO vc_data (title, url, pic) VALUES ( '%s', '%s', '%s' )"
		self.cursor.execute(sql % data)
		self.connect.commit()
		print('成功插入', self.cursor.rowcount, '条数据')
        #return item
