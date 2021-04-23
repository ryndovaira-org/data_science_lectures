import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess


class HabrCompany(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    info = scrapy.Field()
    counter_subscribers = scrapy.Field()
    counter_rating = scrapy.Field()
    tags = scrapy.Field()


class HabrCompaniesSpider(scrapy.Spider):
    name = 'habr_companies'  # spider_name
    allowed_domains = ['habr.com']
    start_urls = ['https://habr.com/ru/companies/']

    def parse(self, response):
        for company in response.css('div.company-info'):
            link = company.css('a.list-snippet__title-link::attr(href)')[0].root.strip()
            counter_subscribers = company.css('div.stats__counter_subscribers::text')[0].root.strip()
            counter_rating = company.css('div.stats__counter_rating::text')[0].root.strip()
            tags = []
            for tag in company.css('span.list-snippet__tags').css('a::text'):
                tags.append(tag.root.strip())
            yield Request(link, callback=self.parse_item_companies,
                          cb_kwargs=dict(counter_subscribers=counter_subscribers,
                                         counter_rating=counter_rating,
                                         tags=tags))

        next_page = response.css('a.arrows-pagination__item-link_next::attr(href)')
        if len(next_page) > 0:
            yield Request('https://habr.com' + next_page[0].root.strip(),
                          callback=self.parse)

    def parse_item_companies(self, response, counter_subscribers, counter_rating, tags):
        link = response.url
        name = response.css('a.page-header__info-title::text')[0].root.strip()
        info = response.css('h2.page-header__info-desc::text')[0].root.strip()

        item = HabrCompany()
        item['name'] = name
        item['link'] = link
        item['info'] = info
        item['counter_subscribers'] = float(counter_subscribers
                                            .replace(',', '.')
                                            .replace('\xa0', '')
                                            .replace('k', '000'))
        item['counter_rating'] = int(counter_rating.replace(',', '').replace('\xa0', ''))
        item['tags'] = tags

        yield item


# if __name__ == '__main__':
#     from scrapy.cmdline import execute
#
#     execute()

if __name__ == '__main__':
    process = CrawlerProcess(settings={
        "FEEDS": {
            # сохранить результаты в файлы
            "./../../habr_companies.json": {"format": "json"},
            "./../../habr_companies.csv": {"format": "csv"},
        },
        "LOG_LEVEL": "ERROR",        # без логов в терминале
        'FEED_EXPORT_ENCODING': 'utf-8'
    })

    process.crawl(HabrCompaniesSpider)

    # the script will block here until the crawling is finished
    process.start()
