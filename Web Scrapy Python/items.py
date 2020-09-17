# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ConsumeraffairsItem(scrapy.Item):
    # define the fields for your item here like:
    user = scrapy.Field()
    rating = scrapy.Field()
    verified_reviewer = scrapy.Field()
    verified_buyer = scrapy.Field()
    review_date = scrapy.Field()
    text = scrapy.Field()
    helpful = scrapy.Field()
    site = scrapy.Field()
    
    