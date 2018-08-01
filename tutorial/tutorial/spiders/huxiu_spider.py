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

    html_file = "/usr/www/scrapy/tutorial/test.log"
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
        print(response.body_as_unicode())

        return
        #print(response.body)

        for sel in response.xpath('//tbody[@id="investment-list"]/tr'):
            #item = HuxiuItem()

            print(sel.xpath('td[@class="cover-info"]/div[@class="avatar square"]/a/@title').extract()[0])
            # print(sel.xpath('div[@class="info"]/div[@class="name"]/a/text()')[0].extract())
            # print(type(sel.xpath('div[@class="info"]/div[@class="name"]/a/text()')[0].extract()))


            # item['title'] = sel.xpath('div[@class="info"]/div[@class="name"]/a/text()')[0].extract()
            # print(item['title'])