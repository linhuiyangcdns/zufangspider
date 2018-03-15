# -*- coding: utf-8 -*-
import scrapy
from zufang.items import ZufangItem

class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['anjuke.com']
    url = "https://hz.zu.anjuke.com/fangyuan/p"
    p = 1
    start_urls = [url + str(p) + "/"]

    def parse(self, response):
        urls = response.xpath('//div[@class="zu-itemmod  "]/@link').extract()
        for full_url in urls:
            yield scrapy.Request(full_url,callback= self.parse_content)
        if len(urls):
            self.p += 1
            yield scrapy.Request(self.url + str(self.p) + "/",callback=self.parse)

    def parse_content(self,response):
        item = ZufangItem()
        item['name'] = response.xpath('//div[@class="wrapper"]/div/h3/text()').extract()[0]
        item['address'] = response.xpath('//div[@class="box"]//dl[5]/dd/a/text()').extract()
        item['price'] = response.xpath('///div[@class="box"]//dd/strong/span/text()') .extract()[0]
        item['typehouse']= response.xpath('//div[@class="box"]//dl[4]/dd/text()').extract()[0]
        item['region'] = response.xpath('//div[@class="box"]//dl[6]/dd/a/text()').extract()
        item['contacts']= response.xpath('//div[@class="rbox"]/div/div/h2/text()').extract()[0]
        item['phone'] = response.xpath('//div[@class="rbox"]/div/p/text()').extract()[0]
        yield item
