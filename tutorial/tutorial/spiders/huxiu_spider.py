#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc :
"""
#from tutorial.items import HuxiuItem
import scrapy
from scrapy.http import Request, FormRequest, HtmlResponse
from scrapy_splash import SplashRequest

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
    # name = "test"
    # allowed_domains = ["jd.com"]
    # start_urls = [
    #     "https://www.jd.com/"
    # ]

    # def parse(self, response):
    #     print(u'---------我这个是简单的直接获取京东网首页测试---------')
    #     guessyou = response.xpath('//div[@class="slider focus_list J_focus_list"]/div[@class="slider_list"]/div[@class="slider_wrapper"]/li//img/@src')
    #     print(guessyou)
    #     print(u'---------------success----------------')

    name = "test"
    allowed_domains = ["jd.com"]
    start_urls = [
        "https://www.jd.com/"
    ]

    def start_requests(self):
        splash_args = {
            'wait': 0.5,
        }
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_result, endpoint='render.html',
                                args=splash_args)

    def parse_result(self, response):
        print(u'----------使用splash爬取京东网首页异步加载内容-----------')
        guessyou = response.xpath('//div[@class="slider focus_list J_focus_list"]/div[@class="slider_list"]/div[@class="slider_wrapper"]/li//img/@src').extract_first()
        print(guessyou)
        print(u'---------------success----------------')

    # def start_requests(self):
    #     yield Request(url = self.start_urls, callback = self.parse)

    # def parse(self, response):
    #     for sel in response.xpath('//tbody[@id="investment-list"]/tr'):
    #         #item = HuxiuItem()
    #         print(sel.xpath('td[@class="cover-info"]/div[@class="avatar square"]/a/@title').extract()[0])