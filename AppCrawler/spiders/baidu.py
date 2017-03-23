# -*- coding:utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from app.items import BaiduAppItem

import re

# the parser class of the Baidu Mobile Phone Assistant
class BaiduSpider(CrawlSpider):
    name = "baidu"
    allowed_domains = ["baidu.com"]
    start_urls = (
        'http://shouji.baidu.com/software/',
    )
    rules = [
        Rule(LinkExtractor(allow=('/software/\d+/$',)), callback='parse_app')
    ]

    # the callback func of BaiduSpider class
    def parse_app(self, response):
        Pagenum = '8'
        self.log("Fetch group home page:%s, %s total page" %(response.url,Pagenum))

        category = response.xpath('//div[@class="sec-breadcrumb"]/a[2]/text()').extract()[0]
        subcategory = response.xpath('//div[@class="sec-breadcrumb"]/span/text()').extract()[0]
        for sel in response.xpath('//div[@class="app-bd"]/ul/li'):
            App = BaiduAppItem()
            App['category'] = category
            App['subcategory'] = subcategory
            App['appname'] = sel.xpath('a/div[@class="app-detail"]/p[@class="name"]/text()').extract()[0]
            App['size'] = sel.xpath('a/div[@class="app-detail"]/p[@class="down-size"]/span[@class="size"]/text()').extract()[0]
            App['downloadnum'] = sel.xpath('a/div[@class="app-detail"]/p[@class="down-size"]/span[@class="down"]/text()').extract()[0]
            praisepercent_ori = sel.xpath('a/div[@class="app-popover"]/div/div[@class="appinfo-left"]/p[@class="star-wrap"]/span/span//@style').extract()[0]
            praisepercent = re.search(r'width:(\d+)', praisepercent_ori).group(1)
            App['praisepercent'] = praisepercent
            yield App

        # Auto generate the next 7 pages' url and add to the url query list
        if re.search(r'/\d+/$', response.url) != None:
            for i in range(2, int(Pagenum)+1):
                url = response.url + 'list_' + str(i) + '.html'
                yield Request(url, callback=self.parse_app)
                self.log("Auto generate the No.%s page: %s" % (str(i), url))
