# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class House(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    property_name = scrapy.Field()
    building_name = scrapy.Field()
    house_name = scrapy.Field()
    plan_purpose = scrapy.Field()
    house_purpose = scrapy.Field()
    floor = scrapy.Field()
    floor_height = scrapy.Field()
    house_orientation = scrapy.Field()
    house_construction = scrapy.Field()
    is_public = scrapy.Field()
    is_back_moving = scrapy.Field()
    is_oneself = scrapy.Field()
    is_pre_sell = scrapy.Field()
    price = scrapy.Field()
    pre_total_square = scrapy.Field()
    actual_total_square = scrapy.Field()
    pre_inner_square = scrapy.Field()
    actual_inner_square = scrapy.Field()
    pre_public_square = scrapy.Field()
    actual_public_square = scrapy.Field()
    is_pledge = scrapy.Field()
    is_seal = scrapy.Field()
    pass
