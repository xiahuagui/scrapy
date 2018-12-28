#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc :
"""
#from tutorial.items import HuxiuItem
import scrapy
from scrapy.http import Request, FormRequest, HtmlResponse

# class HuxiuSpider(scrapy.Spider):
#     name = "huxiu"
#     allowed_domains = ["vc.cn"]
#     #start_urls = "https://www.vc.cn/investments"
#     start_urls = [
#         "https://www.vc.cn/investments"
#     ]

#     def parse(self, response):
#         for sel in response.xpath('//tbody[@id="investment-list"]/tr'):
#             item = HuxiuItem()
#             item['title'] = sel.xpath('td[@class="cover-info"]/div[@class="avatar square"]/a/@title').extract()[0]
#             url = sel.xpath('td[@class="cover-info"]/div[@class="avatar square"]/a/@href').extract()[0]
#             item['url'] = response.urljoin(url)
#             item['pic'] = sel.xpath('td[@class="cover-info"]/div[@class="avatar square"]/a/img/@data-echo').extract()[0]
#             yield item
            
class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["jd.com"]
    start_urls = [
        "https://www.jd.com/"
    ]

    def parse(self, response):
        print(u'---------我这个是简单的直接获取京东网首页测试---------')
        guessyou = response.xpath('//div[@id="J_cate"]/ul[@class="JS_navCtn cate_menu"]/li[1]/a/text()').extract_first()
        print(u"find：%s" % guessyou)
        print(u'---------------success----------------')

    # def start_requests(self):
    #     yield Request(url = self.start_urls, callback = self.parse)

    # def parse(self, response):
    #     for sel in response.xpath('//tbody[@id="investment-list"]/tr'):
    #         #item = HuxiuItem()
    #         print(sel.xpath('td[@class="cover-info"]/div[@class="avatar square"]/a/@title').extract()[0])