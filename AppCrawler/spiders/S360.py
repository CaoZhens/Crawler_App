# -*- coding:utf-8 -*-

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from AppCrawler.items import S360AppItem

import re

class S360AppSpider(CrawlSpider):
    name = 's360'
    allowed_domains = ["360.cn"]
    start_urls = [
        'http://zhushou.360.cn/list/index/cid/1',
    ]

    rules = [
        Rule(LinkExtractor(allow=('/list/index/cid/\d{2}/$',))),
        Rule(LinkExtractor(allow=('/list/index/cid/\d{6}/$',))),
        Rule(LinkExtractor(allow=('/list/index/cid/\d{2}/order/download/\?page=\d+$',)), callback='parse_app', follow=True),
        Rule(LinkExtractor(allow=('/list/index/cid/\d{6}/order/download/\?page=\d+$',)), callback='parse_app', follow=True),
    ]

    # the callback func of S360AppSpider
    def parse_app(self, response):
        category = response.xpath('//div[@class="menu"]/div[@class="menuc"]/h3/text()').extract()[0]
        subcategory = re.search(r'/cid/(\d+)', response.url).group(1)
        for sel in response.xpath('//div[@class="main"]/div/div[@class="icon_box"]/ul[@id="iconList"]/li'):
            app_href = r'http://zhushou.360.cn' + str(sel.xpath('a/@href').extract()[0])
            yield Request(url=app_href, meta={'category': category, 'subcategory': subcategory}, callback=self.parse_app_info)

        # Auto generate the next 50 page and insert into url list
        Pagenum = '50'
        if re.search(r'page=1$', response.url) != None:
            for i in range(2,int(Pagenum)+1):
                url = response.url[:-1] + str(i)
                yield Request(url, callback=self.parse_app)

    def parse_app_info(self, response):
        App = S360AppItem()
        App['category'] = response.meta['category']
        App['subcategory'] = response.meta['subcategory']
        App['appname'] = response.xpath('//div[@id="app-info-panel"]/div/dl/dd/h2/span/text()').extract()[0]
        App['appicon'] = response.xpath('//div[@id="app-info-panel"]/div/dl/dt/img/@src').extract()[0]
        App['size'] = response.xpath('//div[@id="app-info-panel"]/div/dl/dd/div/span[4]/text()').extract()[0]
        App['downloadnum'] = response.xpath('//div[@id="app-info-panel"]/div/dl/dd/div/span[3]/text()').extract()[0]
        App['praisepercent'] = response.xpath('//div[@id="app-info-panel"]/div/dl/dd/div/span[1]/text()').extract()[0]
        App['gdate'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        yield App