from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from random import randint
import os
import fnmatch
import re
import time

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

    urls = {}
    names = {}
    opened = False


    def parse_item(self, response):
        # Apple stars returning 403 if you crawl too fast
        time.sleep(0.1)
        if 'Catalan' not in response.body:
            return

        if '/app/' not in response.url:
            return

        if not self.opened:
            self.html_out = open('urls.htm', "w")
            self.opened = True

        self.html_out.flush()
        num = randint(0, 9)
        
        filename = 'text-' + str(num) + '.log'
        f = open(filename, 'wb')
        f.write(response.body)
        f.close()

        print(filename)
        searchfile2 = open(filename, "r")
        for h1_line in searchfile2:
            if '<h1>' in h1_line:
                r = re.compile('<h1>(.*?)</h1>')
                m = r.search(h1_line)
                url = response.url
                #url = url.replace('mt=','&mt=')
                name = m.group(1) 
                if self.urls.has_key(url) == False and self.names.has_key(name) == False:
                    #itemprop="ratingValue">4.64513</span>
                    r = re.compile('itemprop="ratingValue">(.*?)</span>') 
                    m = r.search(h1_line)
                    if m is not None and m.group.size() > 1:
                        rating = ' (rating {0}) '.format(m.group(1))
                    else:
                        rating = ''
    
                    self.urls[url] = True;
                    self.names[name] = True;
                    self.html_out.write(name + rating + ": " + "<a href=" +url+">" + url + "<a><br/>\n")
				
        		
        os.remove(filename)
