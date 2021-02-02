import scrapy
from scrapy import Request


class HabrNews(scrapy.Item):
    news_id = scrapy.Field()
    title = scrapy.Field()
    hubs = scrapy.Field()
    text = scrapy.Field()
    tags = scrapy.Field()
    author = scrapy.Field()
    author_specialization = scrapy.Field()
    author_karma = scrapy.Field()
    author_rating = scrapy.Field()
    comments_counter = scrapy.Field()


class HabrNewsSpider(scrapy.Spider):
    name = 'habr_news'      # spider_name
    allowed_domains = ['habr.com']
    start_urls = ['https://habr.com/ru/news/']

    def parse(self, response):
        for news in response.css('a.post__title_link'):
            link = news.css('a::attr(href)')[0].root.strip()
            yield Request(link, callback=self.parse_item_news)

        next_page = response.css('a.arrows-pagination__item-link_next::attr(href)')
        if len(next_page) > 0:
            yield Request('https://habr.com' + next_page[0].root.strip(), callback=self.parse)

    def parse_item_news(self, response):
        news_id = response.url.split('/')[-2]
        title = response.css('span.post__title-text::text')[0].root.strip()
        hubs = []
        text = []
        tags = []
        for hub in response.css('a.hub-link::text'):
            hubs.append(hub.root.strip())

        for text_part in response.css('div.post__text').css('p::text'):
            text.append(text_part.root.strip())

        for tag in response.css('a.post__tag::text'):
            tags.append(tag.root.strip())

        author = response.css('span.user-info__nickname::text')[0].root.strip()
        author_specialization = response.css('div.user-info__specialization::text')[0].root.strip()
        author_karma = response.css('div.stacked-counter__value_green::text')[0].root.strip().replace(',', '.')
        author_rating = response.css('div.stacked-counter__value_magenta::text')[0].root.strip().replace(',', '.')

        comments_counter = response.css('span.comments-section__head-counter::text')[0].root.strip()

        item = HabrNews()
        item['news_id'] = int(news_id)
        item['title'] = title
        item['hubs'] = hubs
        item['text'] = text
        item['tags'] = tags
        item['author'] = author
        item['author_specialization'] = author_specialization
        item['author_karma'] = float(author_karma)
        item['author_rating'] = float(author_rating)
        item['comments_counter'] = int(comments_counter)
        yield item


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
