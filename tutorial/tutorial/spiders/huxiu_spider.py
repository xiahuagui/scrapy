#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc :
"""
from tutorial.items import HuxiuItem
import scrapy

class HuxiuSpider(scrapy.Spider):
    name = "huxiu"
    allowed_domains = ["huxiu.com"]
    start_urls = [
        "http://www.huxiu.com/index.php"
    ]

    def start_requests(self):
        print('aaaaaaaaaaaaaaaaaaaaaaaa')
        yield Request(url = self.start_urls, callback = self.parse)

    def parse(self, response):
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
        print('bbbbbbbbbbbbbbbbbbbbbb')
        for sel in response.xpath('//div[@class="mod-info-flow"]/div/div[@class="mob-ctt"]'):
            item = HuxiuItem()
            item['title'] = sel.xpath('h2/a/text()')[0].extract()
            item['url'] = sel.xpath('h2/a/@href')[0].extract()
            url = response.urljoin(item['url'])
            item['desc'] = sel.xpath('div[@class="mob-sub"]/text()')[0].extract()
            print(item['title'],item['url'],item['desc'])