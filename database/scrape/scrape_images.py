import scrapy
from scrapy.crawler import CrawlerProcess
import json

cleanString = lambda x: x.replace("[1]","").replace("[2]","").replace("[3]","").replace("\n","")

class MySpider(scrapy.Spider):

    name = 'myspider'

    allowed_domains = ['ca.wikipedia.org']

    start_urls = ["https://ca.wikipedia.org/wiki/Districtes_i_barris_de_Barcelona"]

    def parse(self, response):
        trs = response.css(".bellataula>tbody>tr")
        for i in range(2, 75):
            if i in [2,6,12,20,23,29,34,45,58,65]:
           
                barri_url = trs[i].css("td a")[2].attrib["href"]
            else:
                barri_url = trs[i].css("td a")[-1].attrib["href"]
           
            yield response.follow(barri_url, callback=self.parse_barri, meta={'id':i-2})

    def parse_barri(self, response):
        
        i = 0
        
        img = "https:"+response.css(".image>img")[i].attrib["src"]
        while "svg" in img.lower() or "flag" in img.lower():
            img = "https:"+response.css(".image>img")[i].attrib["src"]
            i+=1

        print(json.dumps({
            "id":response.meta.get('id'),
            "img":img
        }),",")



c = CrawlerProcess()
c.crawl(MySpider)
c.start()