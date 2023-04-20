import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess


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
    name = "habr_news"  # spider_name
    allowed_domains = ["habr.com"]
    start_urls = ["https://habr.com/ru/news/"]

    def parse(self, response):
        for news in response.css("a.post__title_link"):
            link = news.css("a::attr(href)")[0].root.strip()
            yield Request(link, callback=self.parse_item_news)

        next_page = response.css("a.arrows-pagination__item-link_next::attr(href)")
        if len(next_page) > 0:
            yield Request(
                "https://habr.com" + next_page[0].root.strip(), callback=self.parse
            )

    def parse_item_news(self, response):
        news_id = response.url.split("/")[-2]

        try_title = response.css("span.post__title-text::text")
        if len(try_title):
            title = try_title[0].root.strip()
        else:
            title = ""

        hubs = []
        text = []
        tags = []
        for hub in response.css("a.hub-link::text"):
            hubs.append(hub.root.strip())

        try_text = response.css("div.post__text").css("p::text")
        if len(try_text) == 0:
            try_text = response.css("div.post__text::text")

        if len(try_text) == 0:
            # TODO: добавить такой пример в лекции
            try_text = response.css("div.post__text").css("em::text, h4::text")

        if len(try_text) == 0:
            print("Something wrong!")

        for text_part in try_text:
            text.append(text_part.root.strip())

        for tag in response.css("a.post__tag::text"):
            tags.append(tag.root.strip())

        author = response.css("span.user-info__nickname::text")[0].root.strip()
        author_specialization = response.css("div.user-info__specialization::text")[
            0
        ].root.strip()

        author_karma = "0"
        author_rating = "0"
        for counter in response.css("a.stacked-counter"):
            if (
                counter.css("div.stacked-counter__label::text")[0].root.strip()
                == "Карма"
            ):
                author_karma = (
                    counter.css("div.stacked-counter__value::text")[0]
                    .root.strip()
                    .replace(",", ".")
                )
            elif (
                counter.css("div.stacked-counter__label::text")[0].root.strip()
                == "Рейтинг"
            ):
                author_rating = (
                    counter.css("div.stacked-counter__value::text")[0]
                    .root.strip()
                    .replace(",", ".")
                )
            else:
                print("Something wrong!")

        comments_counter = response.css("span.comments-section__head-counter::text")[
            0
        ].root.strip()

        item = HabrNews()
        item["news_id"] = int(news_id)
        item["title"] = title
        item["hubs"] = hubs
        item["text"] = text
        item["tags"] = tags
        item["author"] = author
        item["author_specialization"] = author_specialization
        try:
            item["author_karma"] = float(author_karma.replace("–", "-"))
        except Exception as ex:
            print("!")
        item["author_rating"] = float(author_rating.replace("–", "-"))
        item["comments_counter"] = int(comments_counter)
        yield item


# if __name__ == '__main__':
#     from scrapy.cmdline import execute
#
#     execute()

if __name__ == "__main__":
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                # сохранить результаты в файлы
                "./../../habr_news.json": {"format": "json"},
                "./../../habr_news.csv": {"format": "csv"},
            },
            "LOG_LEVEL": "ERROR",  # без логов в терминале
            "FEED_EXPORT_ENCODING": "utf-8",
        }
    )

    process.crawl(HabrNewsSpider)

    # the script will block here until the crawling is finished
    process.start()
