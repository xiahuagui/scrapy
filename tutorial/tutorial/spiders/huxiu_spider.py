#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc :
"""
from tutorial.items import HuxiuItem
import scrapy
from scrapy.http import Request, FormRequest, HtmlResponse
import logging
#from scrapy_splash import SplashRequest,SplashMiddleware

class HuxiuSpider(scrapy.Spider):
    logging.getLogger('scrapy.core.scraper').setLevel(logging.WARNING)
    logging.getLogger('scrapy.core.engine').setLevel(logging.WARNING)
    logging.getLogger('scrapy.utils.log').setLevel(logging.WARNING)
    logging.getLogger('scrapy.crawler').setLevel(logging.WARNING)
    logging.getLogger('scrapy.middleware').setLevel(logging.WARNING)
    
    logging.info('aaaaaaaaaaaaaaaaaaaaaa')
    name = "huxiu"
    allowed_domains = ["huxiu.com"]
    #start_urls = "https://www.vc.cn/investments"

    start_urls = [
        "https://www.huxiu.com/" #"https://www.vc.cn/investments"
    ]

    def parse(self, response):
        logging.info('bbbbbbbbbbbbbbbbbbbbbbbbb')
        logging.info(response)
        #print(response.body)
        return
        
        for sel in response.xpath('//tbody[@id="investment-list"]/tr'):
            #item = HuxiuItem()

            print(sel.xpath('td[@class="cover-info"]/div[@class="avatar square"]/a/@title').extract()[0])
            # print(item['title'])

    # def start_requests(self):
    #     print('bbbbbbbbbbbbbbbbbbbbbb')
    #     yield Request(url = self.start_urls, callback = self.parse)

    # def parse(self, response):
    #     print('cccccccccccccccccccccccc')

    #     for sel in response.xpath('//tbody[@id="investment-list"]/tr'):
    #         #item = HuxiuItem()

    #         print(sel.xpath('td[@class="cover-info"]/div[@class="avatar square"]/a/@title').extract()[0])