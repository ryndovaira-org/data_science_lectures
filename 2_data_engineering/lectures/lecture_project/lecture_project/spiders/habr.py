import scrapy
from scrapy import Selector, Request


class HabrSpider(scrapy.Spider):
    name = 'habr'
    allowed_domains = ['habr.com']
    start_urls = ['https://habr.com/ru/']

    companies = []

    def parse(self, response):
        for navigation_link in response.css('li.nav-links__item a::attr(href)'):
            yield Request(navigation_link.root, callback=self.parse_navigation_link)

    def parse_navigation_link(self, response):
        for navigation_link in response.css('div.tabs-menu a::attr(href)'):

            yield Request(navigation_link.root, callback=self.parse_menu_item)
        ...

    def parse_menu_item(self, response):
        for company in response.css('a.list-snippet__title-link::text'):
            self.companies.append(company.root.strip())

        next_page = response.css('a.arrows-pagination__item-link_next').css('a::attr(href)')
        if len(next_page) > 0:
            yield Request('https://habr.com/ru' + next_page[0].root, callback=self.parse_menu_item)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
