import scrapy
import logging

class BooksBasicSpider(scrapy.Spider):
    name = 'books_basic'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html']

    def parse(self, response):
        logging.info(response.url)
        titles = response.xpath('//h3/a/text()').getall()
        urls = response.xpath('//h3/a/@href').getall()
        
        for i in range(len(titles)):
            yield {
                'title': titles[i],
                'url': urls[i]
            }
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)
        
        
