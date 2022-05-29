import boto3
import scrapy
from scrapy.crawler import CrawlerProcess

ids = {
    "Ciutat Vella" : 1,
    "L'Eixample" : 2,
    "Sants-Montjuïc" : 3,
    "Les Corts" : 4,
    "Sarrià-Sant Gervasi" : 5,
    "Gràcia" : 6,
    "Horta - Guinardó" : 7,
    "Nou Barris" : 8,
    "Sant Andreu" : 9,
    "Sant Martí" : 10
}

class MySpider(scrapy.Spider):

    name = 'myspider'

    allowed_domains = ['ajuntament.barcelona.cat']

    start_urls = ['https://ajuntament.barcelona.cat/en/']

    def parse(self, response):
        for district_url in response.css("ul.districtes-wrapper li a::attr(href)").getall():
            yield response.follow(district_url, callback=self.parse_district)

    def parse_district(self, response):

        district_name = response.css('h1::text').getall()[2]

        if district_name in ids:  
            
            news = []
            for title in response.css('div.media-content'):
                news_title = title.css('h3 a::text').get()
                date = title.css('p.date-new::text').get()
                relative_url = title.css('div.media-content h3 a::attr(href)').get()

                single_news = {
                    "title" : news_title,
                    "date" : date,
                    "url" : 'https://ajuntament.barcelona.cat' + relative_url
                }

                news.append(single_news)

            item = {
                "id" : ids[district_name],
                "district_name" : district_name,
                "news" : news
            }

            table.put_item(Item=item)
        
TABLE_NAME = "scraped_news"

dynamodb = boto3.resource('dynamodb', region_name="eu-west-1")
table = dynamodb.Table(TABLE_NAME)

c = CrawlerProcess()
c.crawl(MySpider)
c.start()
print('Done!')
