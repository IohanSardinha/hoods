import scrapy
from scrapy.crawler import CrawlerProcess

class MySpider(scrapy.Spider):

    name = 'myspider'

    allowed_domains = ['ajuntament.barcelona.cat']

    start_urls = ['https://ajuntament.barcelona.cat/en/']

    def parse(self, response):
        for district_url in response.css("ul.districtes-wrapper li a::attr(href)").getall():
            yield response.follow(district_url, callback=self.parse_district)

    def parse_district(self, response):
        print('\nDistrict: ', response.css('h1::text').getall()[2])
        for title in response.css('div.media-content h3 a::text').getall():
            print(title)


c = CrawlerProcess()
c.crawl(MySpider)
c.start()