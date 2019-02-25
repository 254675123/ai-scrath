# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #
    serial_no = scrapy.Field()
    movie_name = scrapy.Field()
    brief = scrapy.Field()
    director = scrapy.Field()
    actor = scrapy.Field()
    category = scrapy.Field()
    place = scrapy.Field()
    time = scrapy.Field()
    star = scrapy.Field()
    evaluation = scrapy.Field()
    description = scrapy.Field()

    pass
