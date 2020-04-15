# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .modules.utils import get_data_from_conf_file
import json


class WebsitesScraperPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        configuration_data_index = getattr(crawler.spider, 'data_index')
        website_data = get_data_from_conf_file(configuration_data_index)
        website_name = website_data.get('website_name')
        return cls(website_name)

    def close_spider(self, spider):
        self.file.close()

    def __init__(self, website_name):
        self.file = open(f"{website_name}.json", 'w')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
