import queue
import threading
import time
from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor, defer

from db.db_connect import connect_mongo_db
from rabbit.consumer import read_rabbit_msg
from rabbit.rabbit_connect import make_exchange_queue_bind
from read_config import get_conf_value

channel, connection = make_exchange_queue_bind()
rabbit_exchange = get_conf_value("RABBIT_MQ", "exchange_name")
rabbit_queue = get_conf_value("RABBIT_MQ", "queue_name")
connect_mongo_db()

locker = threading.RLock()


class AuthorSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "data/authors.json"}
    authors = queue.Queue()
    thread = threading.Thread(target=read_rabbit_msg,
                              args=(channel, rabbit_queue, authors, locker))

    def start_requests(self) -> Iterable[Request]:
        self.thread.start()

        time.sleep(3)
        while self.authors.qsize() > 0:
            print(f"Queue size is {self.authors.qsize()}")
            author = self.authors.get()
            print(f'Scraped author: {author.get("name")}, {author.get("link")}')
            yield scrapy.Request(url=self.start_urls[0] + author.get("link"))


    def parse(self, response, **kwargs):
        for author in response.xpath("/html//div[@class='author-details']"):
            print("Send request to get info about author")
            author_info = {
                "fullname": author.xpath("h3/text()").extract_first(),
                "born_date": author.xpath(
                    "//span[@class='author-born-date']/text()")
                .extract_first(),
                "born_location": author.xpath(
                    "//span[@class='author-born-location']/text()")
                .extract_first(),
                "description": author.xpath(
                    "//div[@class='author-description']/text()")
                .extract_first().strip(),
            }
            print(f"Author name: {author_info['fullname']}")
            yield author_info

    def closed(self, reason):
        self.thread.join()


# run spider AuthorSpider
if __name__ == "__main__":
    runner = CrawlerRunner()
    d = runner.crawl(AuthorSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

