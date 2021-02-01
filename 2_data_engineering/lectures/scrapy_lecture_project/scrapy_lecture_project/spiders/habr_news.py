import scrapy
from scrapy import Request


class HabrPost(scrapy.Item):
    header = scrapy.Field()
    link = scrapy.Field()


class HabrNews(scrapy.Item):
    header = scrapy.Field()
    link = scrapy.Field()


class HabrHub(scrapy.Item):
    header = scrapy.Field()
    link = scrapy.Field()
    subscribers_count = scrapy.Field()
    rating_cout = scrapy.Field()

class HabrAuthor(scrapy.Item):
    fullname = scrapy.Field()
    nickname = scrapy.Field()
    link = scrapy.Field()
    karma_count = scrapy.Field()
    rating_cout = scrapy.Field()

class HabrCompany(scrapy.Item):
    header = scrapy.Field()
    link = scrapy.Field()
    subscribers_count = scrapy.Field()
    rating_cout = scrapy.Field()


class HabrSpider(scrapy.Spider):
    name = 'habr'
    allowed_domains = ['habr.com']
    start_urls = ['https://habr.com/ru/top/']

    def parse(self, response):
        for navigation_link in response.css('a.tabs-menu__item_link'):
            text = navigation_link.css('h3.tabs-menu__item-text::text')[0].root.strip()
            href = navigation_link.css('a::attr(href)')[0].root.strip()
            if text == 'Статьи':
                yield Request(href, callback=self.parse_item_top)
            elif text == 'Новости':
                yield Request(href, callback=self.parse_item_news)
            elif text == 'Хабы':
                yield Request(href, callback=self.parse_item_hubs)
            elif text == 'Авторы':
                yield Request(href, callback=self.parse_item_authors)
            elif text == 'Компании':
                yield Request(href, callback=self.parse_item_companies)

    def parse_item_top(self, response):
        for post in response.css('a.post__title_link'):
            item = HabrPost()
            item['header'] = post.css('a::text')[0].root.strip()
            item['link'] = post.css('a::attr(href)')[0].root.strip()
            yield item

        next_page = response.css('a.arrows-pagination__item-link_next::attr(href)')
        if len(next_page) > 0:
            yield Request('https://habr.com' + next_page[0].root.strip(), callback=self.parse_item_top)

    def parse_item_news(self, response):
        for news in response.css('a.post__title_link'):
            item = HabrNews()
            item['header'] = news.css('a::text')[0].root.strip()
            item['link'] = news.css('a::attr(href)')[0].root.strip()
            yield item

        next_page = response.css('a.arrows-pagination__item-link_next::attr(href)')
        if len(next_page) > 0:
            yield Request('https://habr.com' + next_page[0].root.strip(), callback=self.parse_item_news)

    def parse_item_hubs(self, response):
        for hub in response.css('li.content-list__item_hubs'):
            item = HabrHub()
            item['header'] = hub.css('a.list-snippet__title-link::text')[0].root.strip()
            item['link'] = hub.css('a.list-snippet__title-link::attr(href)')[0].root.strip()
            item['subscribers_count'] = hub.css('div.stats__counter_subscribers::text')[0].root.strip()
            item['rating_cout'] = hub.css('div.stats__counter_rating::text')[0].root.strip()
            yield item

        next_page = response.css('a.arrows-pagination__item-link_next::attr(href)')
        if len(next_page) > 0:
            yield Request('https://habr.com' + next_page[0].root.strip(), callback=self.parse_item_hubs)

    def parse_item_authors(self, response):
        for author in response.css('li.content-list__item_users'):
            item = HabrAuthor()
            item['fullname'] = author.css('a.list-snippet__fullname::text')[0].root.strip()
            item['nickname'] = author.css('a.list-snippet__nickname::attr(href)')[0].root.strip()
            item['link'] = author.css('a.list-snippet__fullname::attr(href)')[0].root.strip()
            item['karma_count'] = author.css('div.stats__counter_karma::text')[0].root.strip()
            item['rating_cout'] = author.css('div.stats__counter_rating::text')[0].root.strip()
            yield item

        next_page = response.css('a.arrows-pagination__item-link_next::attr(href)')
        if len(next_page) > 0:
            yield Request('https://habr.com' + next_page[0].root.strip(), callback=self.parse_item_authors)

    def parse_item_companies(self, response):
        for company in response.css('li.content-list__item_companies'):
            item = HabrCompany()
            item['header'] = company.css('a.list-snippet__title-link::text')[0].root.strip()
            item['link'] = company.css('a.list-snippet__title-link::attr(href)')[0].root.strip()
            item['subscribers_count'] = company.css('div.stats__counter_subscribers::text')[0].root.strip()
            item['rating_cout'] = company.css('div.stats__counter_rating::text')[0].root.strip()
            yield item

        next_page = response.css('a.arrows-pagination__item-link_next::attr(href)')
        if len(next_page) > 0:
            yield Request('https://habr.com' + next_page[0].root.strip(), callback=self.parse_item_companies)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
