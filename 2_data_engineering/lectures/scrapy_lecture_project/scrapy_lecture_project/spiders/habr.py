import scrapy
from scrapy import Selector, Request


class HabrSpider(scrapy.Spider):
    name = 'habr'
    allowed_domains = ['habr.com']
    start_urls = ['https://habr.com/ru/top/']

    companies = []

    # [{'text': 'blablabla', 'href': 'https://....'}]
    posts = []

    # [{'text': 'blablabla', 'href': 'https://....'}]
    news = []

    hubs = []

    authors = []

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
            text = post.css('a::text')[0].root.strip()
            href = post.css('a::attr(href)')[0].root.strip()
            self.posts.append({'text': text, 'href': href})

        next_page = response.css('a.arrows-pagination__item-link_next::attr(href)')
        if len(next_page) > 0:
            yield Request('https://habr.com' + next_page[0].root.strip(), callback=self.parse_item_top)

    def parse_item_news(self, response):
        for news in response.css('a.post__title_link'):
            text = news.css('a::text')[0].root.strip()
            href = news.css('a::attr(href)')[0].root.strip()
            self.news.append({'text': text, 'href': href})

        next_page = response.css('a.arrows-pagination__item-link_next::attr(href)')
        if len(next_page) > 0:
            yield Request('https://habr.com' + next_page[0].root.strip(), callback=self.parse_item_news)

    def parse_item_hubs(self, response):
        for hub in response.css('li.content-list__item_hubs'):
            text = hub.css('a.list-snippet__title-link::text')[0].root.strip()
            href = hub.css('a.list-snippet__title-link::attr(href)')[0].root.strip()
            subscribers_count = hub.css('div.stats__counter_subscribers::text')[0].root.strip()
            rating_cout = hub.css('div.stats__counter_rating::text')[0].root.strip()

            self.hubs.append({'text': text,
                              'href': href,
                              'subscribers_count': subscribers_count,
                              'rating_cout': rating_cout})

        next_page = response.css('a.arrows-pagination__item-link_next::attr(href)')
        if len(next_page) > 0:
            yield Request('https://habr.com' + next_page[0].root.strip(), callback=self.parse_item_hubs)

    def parse_item_authors(self, response):
        for author in response.css('li.content-list__item_users'):
            text = author.css('a.list-snippet__fullname::text')[0].root.strip()
            nick = author.css('a.list-snippet__nickname::attr(href)')[0].root.strip()
            href = author.css('a.list-snippet__fullname::attr(href)')[0].root.strip()
            karma_count = author.css('div.stats__counter_karma::text')[0].root.strip()
            rating_cout = author.css('div.stats__counter_rating::text')[0].root.strip()

            self.authors.append({'text': text,
                                 'nick': nick,
                                 'href': href,
                                 'karma_count': karma_count,
                                 'rating_cout': rating_cout})

        next_page = response.css('a.arrows-pagination__item-link_next::attr(href)')
        if len(next_page) > 0:
            yield Request('https://habr.com' + next_page[0].root.strip(), callback=self.parse_item_authors)

    def parse_item_companies(self, response):
        for company in response.css('li.content-list__item_companies'):
            text = company.css('a.list-snippet__title-link::text')[0].root.strip()
            href = company.css('a.list-snippet__title-link::attr(href)')[0].root.strip()
            subscribers_count = company.css('div.stats__counter_subscribers::text')[0].root.strip()
            rating_cout = company.css('div.stats__counter_rating::text')[0].root.strip()

            self.companies.append({'text': text,
                                   'href': href,
                                   'subscribers_count': subscribers_count,
                                   'rating_cout': rating_cout})

        next_page = response.css('a.arrows-pagination__item-link_next::attr(href)')
        if len(next_page) > 0:
            yield Request('https://habr.com' + next_page[0].root.strip(), callback=self.parse_item_companies)


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
