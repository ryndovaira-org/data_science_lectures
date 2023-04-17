import scrapy


class ExampleSpider(scrapy.Spider):
    name = "examples"
    allowed_domains = ["examples.com"]
    start_urls = ["http://example.com/"]

    def parse(self, response):
        pass
