from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class MySpider(CrawlSpider):

    cnt = 0
    """ Crawl through web sites you specify """

    name = "mycrawler"

    # Stay within these domains when crawling
    allowed_domains = ["itunes.apple.com"]

    start_urls = [
    "https://itunes.apple.com/md/genre/ios/id36?mt=8",
    ]

    # Add our callback which will be called for every found link
    rules = [
    Rule(SgmlLinkExtractor(), follow=True,callback='parse_item')
    ]

    def parse_item(self, response):
        if 'Catalan'  not in response.body:
            return

        with open('text-' + str(self.cnt) + '.log', 'wb') as f:
            f.write(response.url + "\n")
            f.write(response.body)

        self.cnt = self.cnt + 1
