# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserTrendItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()  
    time = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()    
