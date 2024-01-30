from quotes.quotes.spiders.author import AuthorSpider
from quotes.quotes.spiders.quote import QuotesSpider

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
configure_logging(settings)
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(QuotesSpider)
    yield runner.crawl(AuthorSpider)
    reactor.stop()


if __name__ == "__main__":
    crawl()
    reactor.run()
