# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

#class AppcrawlerPipeline(object):
#    def process_item(self, item, spider):
#        return item

class AppcrawlerPipeline(object):
    def __init__(self):
        # Set MongoDB link
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # login
        #self.client.admin.authenticate(settings['MONGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]
        self.coll = self.db[settings['MONGO_COLL_BAIDU']]

    def process_item(self, item, spider):
        postItem = dict(item)
        self.coll.insert(postItem)
        return item
