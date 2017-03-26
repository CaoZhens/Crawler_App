# -*- coding:utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from AppCrawler.items import TencentAppItem

import re
import time

# the parser class of the Tencent App Assistant
class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ["qq.com"]
    start_urls = [
        'http://sj.qq.com/myapp/category.htm?orgame=1',
    ]
    rules = [
        Rule(LinkExtractor(allow=("\?orgame=\d+&categoryId=\d+",)), callback='parse_app'),
        #Rule(LinkExtractor(allow=("\?orgame=\d+&categoryId=-\d+",)), callback='parse_app'),
        #Rule(LinkExtractor(allow=("\?apkName=")), callback='parse_app_info'),
    ]

    def get_downloadnum(self, obj):
        obj = obj.encode('utf-8')
        if re.search(r'\d+\.*\d*', obj):
            absolutenum = re.search(r'\d+\.*\d*', obj).group(0)
            unit = 0.0001
            if re.search(r'\xe4\xb8\x87', obj):
                unit = 1
            if re.search(r'\xe4\xba\xbf', obj):
                unit = 10000
            return float(absolutenum) * float(unit)
        else:
            return 0

    def get_size(self, obj):
        obj = obj.encode('utf-8')
        if re.search(r'\d+\.*\d*', obj):
            absolutenum = re.search(r'\d+\.*\d*', obj).group(0)
            unit = 1
            if re.search(r'M', obj):
                unit = 1
            if re.search(r'K', obj):
                unit = 1.0 / 1024
            return float(absolutenum) * float(unit)
        else:
            return 0

    # the callback func (mid) of TencentSpider class
    def parse_app(self, response):
        category = response.xpath('//div[@class="com-nav"]/div/ul//a[@class="com-nav-btn selected"]/text()').extract()[0]
        for sel in response.xpath('//div[@class="main"]/ul[@class="app-list clearfix"]/li'):
            app_href = r'http://sj.qq.com/myapp/' + str(sel.xpath('div[@class="app-info clearfix"]/a/@href').extract()[0])
            yield Request(url=app_href, meta={'category':category}, callback=self.parse_app_info)

        #Auto detect the next page, then generate the url and insert into url list
        if re.search(r'window.pageContext = (\d+)', response.xpath('//body/script[1]/text()').extract()[0]):
            PageContext = re.search(r'window.pageContext = (\d+)', response.xpath('//body/script[1]/text()').extract()[0]).group(1)
            url_prefix = re.search(r'http://sj.qq.com/myapp/category.htm\?categoryId=\d+&orgame=\d+', response.url)
            url = url_prefix.group(0) + '&pageContext=' + str(PageContext)
            yield Request(url, callback=self.parse_app)
            self.log("Auto generate the page : %s" % url)

    def parse_app_info(self, response):
        App = TencentAppItem()
        App['category'] = response.meta['category']
        App['subcategory'] = response.xpath('//div[@class="det-type-box"]/a/text()').extract()[0]
        App['appname'] = response.xpath('//div[@class="det-name"]/div[@class="det-name-int"]/text()').extract()[0]
        App['appicon'] = response.xpath('//div[@class="det-icon"]/img/@src').extract()[0]
        App['size'] = response.xpath('//div[@class="det-insnum-line"]/div[3]/text()').extract()[0]
        App['size'] = self.get_size(App['size'])
        App['downloadnum'] = response.xpath('//div[@class="det-insnum-line"]/div[1]/text()').extract()[0]
        App['downloadnum'] = self.get_downloadnum(App['downloadnum'])
        App['praisepercent'] = re.search(r'\d+\.*\d*', response.xpath('//div[@class="det-star-box"]/div[2]/text()').extract()[0]).group(0)
        App['praisepercent'] = float(App['praisepercent']) * float(20.0)
        App['gdate'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        yield App


