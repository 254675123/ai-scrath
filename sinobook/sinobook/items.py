# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinobookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # defile the fields
    catalog_code = scrapy.Field()
    catalog_name = scrapy.Field()
    course_name = scrapy.Field()
    pass
