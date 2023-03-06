# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserJobItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    #salary = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    vacancy_link = scrapy.Field()
    #vacancy_len = scrapy.Field()
    #vacancy_links = scrapy.Field()
