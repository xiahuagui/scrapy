#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc :
"""
from tutorial.items import HuxiuItem
import scrapy
from scrapy.http import Request, FormRequest, HtmlResponse
#from scrapy_splash import SplashRequest,SplashMiddleware

class HuxiuSpider(scrapy.Spider):
    print('aaaaaaaaaaaaaaaaaaaaaa')
    name = "huxiu"
    allowed_domains = ["vc.cn"]
    #start_urls = "https://www.vc.cn/investments"

    start_urls = [
        "https://www.vc.cn/investments"
    ]

    def parse(self, response):
        print('bbbbbbbbbbbbbbbbbbbbbbbbb')
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