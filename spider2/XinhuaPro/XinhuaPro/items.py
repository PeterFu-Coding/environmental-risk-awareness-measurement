# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XinhuaproItem(scrapy.Item):
    keyword = scrapy.Field()
    title = scrapy.Field()
    info = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    id = scrapy.Field()
    pass
