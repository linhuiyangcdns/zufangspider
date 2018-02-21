# -*- coding: utf-8 -*-
import scrapy

from tianying.items import TianyingItem


class TiantangSpider(scrapy.Spider):
    name = 'tiantang'
    allowed_domains = ['dytt8.net']
    urls = 'http://www.dytt8.net/html/gndy/dyzz/list_23_'
    offser = 1
    start_urls = [urls + str(offser) + '.html']

    def parse(self, response):
        links = response.xpath('//td/b/a/@href').extract()
        for link in links:
            link1 = 'http://www.dytt8.net%s' % link
            yield scrapy.Request(link1,callback=self.parse_content)
        if self.offser <= 50:
            self.offser += 1
            yield scrapy.Request(self.urls + str(self.offser) + '.html',callback=self.parse)

    def parse_content(self, response):
        item = TianyingItem()
        item['name'] = response.xpath("//div[@class='title_all']/h1/font/text()").extract()[0]
        item['href'] = response.xpath('//tbody/tr/td[@style="WORD-WRAP: break-word"]/a').extract()

        yield item
