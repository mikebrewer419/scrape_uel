# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    volume = scrapy.Field()
    year = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    pdf_url = scrapy.Field()
    issn = scrapy.Field()
