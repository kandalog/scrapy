import scrapy

class FantasySpider(scrapy.Spider):
    name = 'fantasy'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html']

    def parse(self, response):
        # 起点のxpath
        books = response.xpath('//section/div/ol[@class="row"]/li')
        
        for book in books:
            # yield {
            #     'title': book.xpath('.//h3/a/text()').get(),
            #     'price': book.xpath('.//p[@class="price_color"]/text()').get(),
            #     'url': book.xpath('.//h3/a/@href').get()
            # }
            yield response.follow(url=book.xpath('.//h3/a/@href').get(), callback=self.parse_item)
    
        # 次のページがあればスクレイピングする
        next_page = response.xpath('//li[@class="next"]/a/@href')
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)

    # 詳細ページのスクレイピング
    def parse_item(self, response):
        basic = response.xpath('//div[@class="col-sm-6 product_main"]')
        yield {
            # セレクターに対してxpathを指定する場合 . が必要
            'title': basic.xpath('.//h1/text()').get(),
            'price': basic.xpath('.//p[@class="price_color"]/text()').get(),
            'judge': basic.xpath('.//p[3]/@class').get(),
            'UCP': basic.xpath('//th[contains(text(), "UPC")]/following-sibling::td/text()').get(),
            'Number-of-stars': basic.xpath('//th[contains(text(), "Number of reviews")]/following-sibling::td/text()').get()
        }