# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from AppCrawler.items import GooglePlayAppItem

class GoogleSpider(CrawlSpider):
    name = "google"
    allowed_domains = ["play.google.com"]
    start_urls = [
        'http://play.google.com/',
        'https://play.google.com/store/apps/details?id=com.viber.voip',
    ]
    rules = [
        Rule(LinkExtractor(allow=('https://play\.google\.com/store/apps/details')), callback='parse_app', follow=True),
    ]

    def parse(self, response):
        App = GooglePlayAppItem()
        App['subcategory'] = response.xpath('//a[@class="document-subtitle category"]/span[@itemprop="genre"]/text()')
        App['appname'] = response.xpath('//div[@class="id-app-title"]/text()')
        App['appicon'] = response.xpath('//div[@class="cover-container"]/img/@src')
        App['downloadnum'] = response.xpath('//div[@itemprop="numDownloads"]/text()')
        praisepercent_ori = response.xpath('//div[@class="current-rating"]/@style').extract()[0]
        praisepercent = re.search(r'width:(\d+)', praisepercent_ori).group(1)
        App['praisepercent'] = float(praisepercent)
        App['gdate'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        yield App
