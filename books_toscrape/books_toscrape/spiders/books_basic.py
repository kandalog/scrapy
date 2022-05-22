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
            # yield {
            #     'title': titles[i],
            #     'url': urls[i]
            # }

            # yield response.followで詳細ページにアクセス
            # 詳細ページ用のcallback関数を作成して渡す
            yield response.follow(url=urls[i], callback=self.parse_item)
        
        # リンク
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)
        
    
    # callbackで渡す関数を定義
    # 詳細ページの情報を引っ張ってくる
    # response.xpath部分を直接yieldに渡しても良いかも
    def parse_item(self, response):
        title = response.xpath('//h1/text()').get()
        price = response.xpath('//div[contains(@class, "product_main")]//p[@class="price_color"]/text()').get()
        stock = response.xpath('//div[@class="col-sm-6 product_main"]//p[@class="instock availability"]/text()[2]').get()
        rating = response.xpath('//p[contains(@class, "star-rating")]/@class').get()
        upc = response.xpath('//th[contains(text(), "UPC")]/following-sibling::td/text()').get()
        review = response.xpath('//th[contains(text(), "Number of reviews")]/following-sibling::td/text()').get()
        yield {
            'title': title,
            'price': price,
            'stock': stock,
            'rating': rating,
            'upc': upc,
            'review': review
        }
