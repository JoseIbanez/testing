import scrapy


class PwspiderSpider(scrapy.Spider):
    name = "pwspider"
    allowed_domains = ["www.marca.com"]
    start_urls = "https://www.marca.com/programacion-tv.html?intcmp=MENUDEST&s_kw=agenda-tv"


    def start_requests(self):
        yield scrapy.Request(self.start_urls, meta={'playwright': True})

    def parse(self, response):

        yield {
            'text': response.css('ol').getall(),
        }

