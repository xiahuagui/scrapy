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
    start_urls = "https://www.vc.cn/investments"
    # start_urls = [
    #     "https://www.vc.cn/investments"
    # ]

    # def parse(self, response):
    #     print('bbbbbbbbbbbbbbbbbbbbbbbbb')
    #     for sel in response.xpath('//tbody[@class="investment-list"]/tr'):
    #         item = HuxiuItem()

    #         print(sel.xpath('div[@class="info"]/div[@class="name"]/a/text()'))
    #         print(sel.xpath('div[@class="info"]/div[@class="name"]/a/text()')[0].extract())
    #         print(type(sel.xpath('div[@class="info"]/div[@class="name"]/a/text()')[0].extract()))


    #         item['title'] = sel.xpath('div[@class="info"]/div[@class="name"]/a/text()')[0].extract()
    #         print(item['title'])

    def start_requests(self):
        print('bbbbbbbbbbbbbbbbbbbbbb')
        yield Request(url = self.start_urls, callback = self.parse)

    def parse(self, response):
        print('cccccccccccccccccccccccc')
        print(response)
        print(type(response))
        print(response.xpath('//header/text()').extract()[0])
        print(type(response.xpath('//header/text()').extract()[0]))

        # for sel in response.xpath('//tbody[@class="investment-list"]/tr'):
        #     item = HuxiuItem()

        #     print(sel.xpath('div[@class="info"]/div[@class="name"]/a/text()'))
        #     print(sel.xpath('div[@class="info"]/div[@class="name"]/a/text()')[0].extract())
        #     print(type(sel.xpath('div[@class="info"]/div[@class="name"]/a/text()')[0].extract()))


        #     item['title'] = sel.xpath('div[@class="info"]/div[@class="name"]/a/text()')[0].extract()
        #     print(item['title'])