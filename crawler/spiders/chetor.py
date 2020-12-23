import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from crawler.items import ArticleItem, CommentItem
from scrapy.loader import ItemLoader



class ChetorSpider(CrawlSpider):
    name = 'chetor'
    # name = 'tutsplus'
    allowed_domains = ['chetor.com']
    start_urls = ['https://chetor.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@class='post-url post-title']"), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_xpaths="//a[@class='pagination__button pagination__next-button']"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
    
        # comments = []
        self.logger.info(f"this is the url :{response.url}")
        comments = ItemLoader(  
                            item=CommentItem(), 
                            selector=response.selector.xpath("//div[@class='comments-wrap']"), 
                            response=response
                            )
        for comment in response.selector.xpath("//div[@class='comments-wrap']"):
            # comments = ItemLoader(item=CommentItem(), selector=comment, response=response)
            comments.add_xpath('username', ".//cite[@class='comment-author']/text()")
            comments.add_xpath('publish', ".//time[@class='comment-published']/@datetime")
            comments.add_xpath('content', ".//div[@class='comment-content']/p/text()")
            
        

        # yield comments.load_item()

        body = response.selector.xpath("/html/body")
        article = ItemLoader(item=ArticleItem(), selector=body, response=response)
        article.add_xpath('title', "//span[@class='post-title']/text()")
        article.add_xpath('body', "//div[@class='entry-content clearfix single-post-content']")
        article.add_xpath('author', '//span[@class="post-author-name"]/b/text()')
        article.add_xpath('lastmodified', '//div[@class="post-meta single-post-meta"]/span/time/@datetime')
        article.add_xpath('readin', '//span[@class="no-line"]/b[1]/text()')
        article.add_xpath('tags', '//div[@class="entry-terms post-tags clearfix "]/a/text()')
        article.add_value('slug', response.request.url.split('/')[-2])
        article.add_value('comments', comments.load_item())
        
        return article.load_item()
        
