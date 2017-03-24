# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BaiduAppItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    appname = scrapy.Field()
    appicon = scrapy.Field()
    size = scrapy.Field()
    downloadnum = scrapy.Field()
    praisepercent = scrapy.Field()
    gdate = scrapy.Field()

class TencentAppItem(scrapy.Item):
    category = scrapy.Field()
    subcategory = scrapy.Field()
    appname = scrapy.Field()
    appicon = scrapy.Field()
    size = scrapy.Field()
    downloadnum = scrapy.Field()
    praisepercent = scrapy.Field()
    gdate = scrapy.Field()

class S360App1Item(scrapy.Item):
    categoryId = scrapy.Field()
    softId = scrapy.Field()
    appname = scrapy.Field()

class S360App2Item(scrapy.Item):
    softId = scrapy.Field()
    appname = scrapy.Field()
    size = scrapy.Field()
    downloadnum = scrapy.Field()
    praisescore = scrapy.Field()
    gdate = scrapy.Field()

class IqiyiItem(scrapy.Item):
    title = scrapy.Field()
    urllink = scrapy.Field()
    Is1080P = scrapy.Field()
