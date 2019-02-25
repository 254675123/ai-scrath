# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanMovieSpider(scrapy.Spider):
    # spider name
    name = 'douban_movie'

    # allow domain name
    allowed_domains = ['movie.douban.com']

    # the input url
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        # print(response.text)

        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i_item in movie_list:
            movie_item = DoubanItem()
            movie_item['serial_no'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            movie_item['movie_name'] = i_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            movie_content = i_item.xpath(".//div[@class='bd']/p[1]/text()").extract()

            # director, actor, place, time, and so on
            movie_brief = ''
            for sub_content in movie_content:
                content_list = sub_content.split()
                movie_brief = movie_brief + '; ' + ''.join(content_list)

            movie_item['brief'] = movie_brief
            # star, evaluation
            movie_item['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
            movie_item['evaluation'] = i_item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            movie_item['description'] = i_item.xpath(".//p[@class='quote']/span/text()").extract_first()

            yield movie_item

        # next page
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link_0 = next_link[0]
            yield scrapy.Request(self.start_urls[0]+next_link_0, callback=self.parse)
