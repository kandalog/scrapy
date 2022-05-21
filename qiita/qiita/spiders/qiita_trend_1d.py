import scrapy


class QiitaTrend1dSpider(scrapy.Spider):
    name = 'qiita_trend_1d' # 一意の名前
    allowed_domains = ['qiita.com'] # アクセスするアドレス
    start_urls = ['https://qiita.com/'] # 最初のアドレス

    # レスポンスが返ってくる
    def parse(self, response):
        category = response.xpath('//a[@class="st-NewHeader_mainNavigationItem is-active"]/text()').get()
        titles = response.xpath('//h2[@class="css-1t4fpk1"]/a/text()').getall()
        urls = response.xpath('//h2[@class="css-1t4fpk1"]/a/@href').getall()
        
        for i in range(len(titles)):
            yield {
                'category': category,
                'titles': titles[i],
                'urls': urls[i]
            }
