# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZufangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()#名称
    address = scrapy.Field()#地址
    price = scrapy.Field()#价格
    typehouse = scrapy.Field()#房屋类型
    region = scrapy.Field()#区域
    contacts = scrapy.Field()#联系人
    phone = scrapy.Field()#电话号码
