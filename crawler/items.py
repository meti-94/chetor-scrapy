# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import tomd


class CommentItem(scrapy.Item):
    

    username = scrapy.Field()
    publish = scrapy.Field()
    content = scrapy.Field()


# tostring = lambda text:text[9:14]

class ArticleItem(scrapy.Item):
    comments = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    author = scrapy.Field()
    lastmodified = scrapy.Field()
    readin = scrapy.Field()
    tags = scrapy.Field()
    slug = scrapy.Field()    