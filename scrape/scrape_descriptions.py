import scrapy
from scrapy.crawler import CrawlerProcess
import json

class MySpider(scrapy.Spider):

    name = 'myspider'

    allowed_domains = ['en.wikipedia.org']

    start_urls = ["https://en.wikipedia.org/wiki/Districts_of_Barcelona"]

    def parse(self, response):
        trs = response.css(".wikitable>tbody>tr")
        for i in range(2, 75):
            barri_url = trs[i].css("td a")[-1].attrib["href"]
            yield response.follow(barri_url, callback=self.parse_barri, meta={'id':i-2})

    def parse_barri(self, response):
        first_paragraph = " ".join(response.css("#mw-content-text>div>p")[0].css("*::text").extract())
        second_paragraph = " ".join(response.css("#mw-content-text>div>p")[1].css("*::text").extract())
        
        print(json.dumps({
            "id":response.meta.get('id'),
            "description":first_paragraph+"\n"+second_paragraph
        }),",")



c = CrawlerProcess()
c.crawl(MySpider)
c.start()