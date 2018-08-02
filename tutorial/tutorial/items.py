# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HuxiuItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()  	#标题
    url = scrapy.Field()		#链接
    pic = scrapy.Field()		#图片
