# -*- coding: utf-8 -*-
import scrapy
from items import SinobookItem
from browsers import chrome
import pipelines

class CatalogBookSpider(scrapy.Spider):
    name = 'catalog_book'
    allowed_domains = ['sinobook.com.cn']
    start_urls = ['http://www.sinobook.com.cn/b2c/scrp/bookcm.cfm?iClass=1&sMdId=t']
    pre_url = 'http://www.sinobook.com.cn/b2c/scrp/'

    browser_driver = chrome.getBrowser()

    course_list = []

    def parse(self, response):
        # //table[@id='tblCat']//tr/td/li/a/@href
        # catalog_list = response.xpath("//table[@id='tblCat']/").extract()
        catalog_list = response.xpath("//table[@id='tblCat']//tr/td/li/a/@href").extract()
        url_list = []
        for catalog_url in catalog_list:
            # new url
            # catalog_url_list = i_item.xpath(".//tr/td/li/a/@href").extract()
            # for catalog_url in catalog_url_list:

            #yield scrapy.Request(self.pre_url + catalog_url, callback=self.parse_catalog)
            #yield scrapy.Request(self.pre_url + catalog_url, callback=self.parse_catalog_selenium)
            url_list.append(self.pre_url + catalog_url)

        pipelines.fileSaver(url_list, 'need_scratch_urls')


    def parse_catalog(self, response):

        catalog_code = response.xpath("//form/input[@name='sCid']/@value").extract_first()
        # catalog_name = response.xpath("//form/input[@name='sCname']/@value").extract_first()
        course_list = response.xpath("//table[@class='tblBrow']//table//tr[1]/td[@class='tdbn']/a/text()").extract()

        for i_course_name in course_list:
            course_item = SinobookItem()
            course_item['catalog_code'] = catalog_code
            course_item['catalog_name'] = ''
            course_item['course_name'] = i_course_name



            yield course_item



    def parse_catalog_selenium(self, response):

        self.course_list = []
        chrome.getRequest(self.browser_driver, response.url)

        catalog_code = self.browser_driver.find_element_by_name("sCid").get_attribute("value")
        catalog_name = self.browser_driver.find_element_by_name("sCname").get_attribute("value")
        # has next page
        hasNextPage = True
        while hasNextPage:


            course_list = self.browser_driver.find_elements_by_xpath("//*[@class='tdbn']/a")

            for i_course_name in course_list:
                si = SinobookItem()
                si['catalog_code'] = catalog_code
                si['catalog_name'] = ''
                si['course_name'] = i_course_name.text

                self.course_list.append('{} {}'.format(catalog_code, i_course_name.text))

                yield si

            # net page
            hasNextPage = chrome.clickElementByPartText(self.browser_driver, "下一页")


        # save data

        pipelines.fileSaver(self.course_list)

        #self.browser_driver.quit()
