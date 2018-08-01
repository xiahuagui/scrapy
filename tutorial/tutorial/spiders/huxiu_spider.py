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
    name = "huxiu"
    allowed_domains = ["vc.cn"]
    #start_urls = "https://www.vc.cn/investments"
    start_urls = [
        "https://www.vc.cn/investments"
    ]

    def parse(self, response):
        for sel in response.xpath('//tbody[@class="investment-list"]/tr'):
            item = HuxiuItem()
            item['title'] = sel.xpath('div[@class="info"]/div[@class="name"]/a/text()')[0].extract()
            print(item['title'])

    # def start_requests(self):
    #     print('aaaaaaaaaaaaaaaaaaaaaaaa')
    #     yield Request(url = self.start_urls, callback = self.parse)

    #def parse(self, response):
        # print(response)
        # print(type(response))
        # for sel in response.xpath('//div[@class="mod-info-flow"]/div[@class="clearfix"]'):
        #     item = HuxiuItem()
        #     item['pic'] = sel.xpath('div[@class="mod-thumb"]/a/img/@src')[0].extract()
        #     item['url'] = sel.xpath('div[@class="mod-thumb"]/a/@href')[0].extract()
        #     url = response.urljoin(item['url'])
        #     item['title'] = sel.xpath('div[@class="mob-ctt"]/h2/a/text()')[0].extract()
        #     item['desc'] = sel.xpath('div[@class="mob-ctt"]/div[@class="mob-sub"]/text()')[0].extract()
        #     print(item['title'],item['url'],item['desc'],item['pic'])
        #print('bbbbbbbbbbbbbbbbbbbbbb')
        # for sel in response.xpath('//div[@class="mod-info-flow"]/div/div[@class="mob-ctt"]'):
        #     item = HuxiuItem()
        #     item['title'] = sel.xpath('h2/a/text()')[0].extract()
        #     item['url'] = sel.xpath('h2/a/@href')[0].extract()
        #     url = response.urljoin(item['url'])
        #     item['desc'] = sel.xpath('div[@class="mob-sub"]/text()')[0].extract()
        #     print(item['title'],item['url'],item['desc'])