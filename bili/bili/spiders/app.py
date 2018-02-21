# -*- coding: utf-8 -*-
import scrapy
import json
from bili.items import BiliItem


class AppSpider(scrapy.Spider):
    name = 'app'
    allowed_domains = ['api.live.bilibili.com']
    starturl = "https://api.live.bilibili.com/mobile/rooms?actionKey=appkey&appkey=27eb53fc9058f8c3&area_id="
    end_url = "&platform=ios&build=6530&page="
    page = 1
    area_id = 1
    start_urls = [starturl +str(area_id) + end_url+ str(page)]

    def parse(self, response):
        data = json.loads(response.text)['data']
        for each in data:
            item = BiliItem()
            item["area"] = each["area"]
            #item["srcimage"] = each["src"]
            #item["name"] = each["name"]
            item["title"] = each["title"]

            yield item
        if len(data):
            self.page += 1
        else:
            self.area_id +=1
            self.page = 1
        yield scrapy.Request(self.starturl +str(self.area_id) + self.end_url+ str(self.page), callback=self.parse)


