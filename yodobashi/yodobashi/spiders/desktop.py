import scrapy
import logging

class DesktopSpider(scrapy.Spider):
    name = 'desktop'
    allowed_domains = ['www.yodobashi.com']
    start_urls = ['https://www.yodobashi.com/category/19531/11970/34646/']

    def parse(self, response):
        logging.info(response.request.headers['User-Agent'])
        logging.info(response.url)
        # productsにはセレクターobjが格納されている
        products = response.xpath('//div[contains(@class, "productListTile")]')
        for product in products: # productには1つずつ商品情報の塊が入る
            # セレクターobjにxpathを記述する場合最初に.が必要
            maker = product.xpath('.//p[1]/text()').get()
            name = product.xpath('.//p[2]/text()').get()
            price = product.xpath('.//span[@class="productPrice"]/text()').get()
            yield {
                'maker': maker,
                'name': name,
                'price': price
            }
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)