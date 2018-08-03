#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc :
"""
from tutorial.items import HuxiuItem
import scrapy
from scrapy.http import Request, FormRequest, HtmlResponse

class HuxiuSpider(scrapy.Spider):
    name = "huxiu"
    allowed_domains = ["vc.cn"]
    #start_urls = "https://www.vc.cn/investments"
    start_urls = [
        "https://www.vc.cn/investments"
    ]

    def parse(self, response):
        for sel in response.xpath('//tbody[@id="investment-list"]/tr'):
            item = HuxiuItem()
            item['title'] = sel.xpath('td[@class="cover-info"]/div[@class="avatar square"]/a/@title').extract()[0]
            url = sel.xpath('td[@class="cover-info"]/div[@class="avatar square"]/a/@href').extract()[0]
            item['url'] = response.urljoin(url)
            item['pic'] = sel.xpath('td[@class="cover-info"]/div[@class="avatar square"]/a/img/@data-echo').extract()[0]
            yield item
            

    # def start_requests(self):
    #     yield Request(url = self.start_urls, callback = self.parse)

    # def parse(self, response):
    #     for sel in response.xpath('//tbody[@id="investment-list"]/tr'):
    #         #item = HuxiuItem()
    #         print(sel.xpath('td[@class="cover-info"]/div[@class="avatar square"]/a/@title').extract()[0])