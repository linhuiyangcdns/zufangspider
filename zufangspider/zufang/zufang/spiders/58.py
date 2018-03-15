# -*- coding: utf-8 -*-

import scrapy
from zufang.items import ZufangItem


class SpiderSpider(scrapy.Spider):
    name = '58'
    allowed_domains = ['hz.58.com']
    url = "http://hz.58.com/chuzu/pn"
    pn = 1
    start_urls = [url + str(pn)]

    def parse(self, response):
        urls = response.xpath('//div[@class="listBox"]/ul/li/div/h2/a/@href').extract()
        for full_url in urls:
            yield scrapy.Request(full_url,callback= self.parse_content)
        if len(urls):
            self.pn += 1
            yield scrapy.Request(self.url + str(self.pn),callback=self.parse)

    def parse_content(self,response):
        item = ZufangItem()
        item['name'] = response.xpath('//div[@class="house-title"]/h1/text()').extract()[0]
        item['address'] = response.xpath('//div[@class="house-desc-item fl c_333"]/ul/li[3]/span/text()').extract()
        item['price'] = response.xpath('//div[@class="house-desc-item fl c_333"]/div/span/b/text()') .extract()[0]
        item['typehouse']= response.xpath('//div[@class="house-desc-item fl c_333"]/ul/li[1]/span/text()').extract()
        item['region'] = response.xpath('//div[@class="house-desc-item fl c_333"]/ul/li[4]/span/a/text()').extract()[0]
        item['contacts']= response.xpath('//div[@class="house-agent-info fr"]/p/a/text()').extract()[0]
        item['phone'] = response.xpath('//div[@class="house-chat-phone"]/span/text()').extract()[0]
        yield item
