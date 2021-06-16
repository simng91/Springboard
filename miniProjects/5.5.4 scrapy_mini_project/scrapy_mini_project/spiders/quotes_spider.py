import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    # if command line arguments indicate -a tag = " " 
    # so Spider fetch only quotes with specific tag
    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    # start_urls = [
    #     'http://quotes.toscrape.com/page/1/',
    #     'http://quotes.toscrape.com/page/2/',
    # ]
    start_urls = ['http://quotes.toscrape.com/']

    # Spider can automatically generate requests by the above given URLS without this method below
    # callback method to parse is known by default for Spider
    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    # This below method only save the responses to HTML files (no data extraction)
    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)

    # data extraction
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        # OPTION 1
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            #next_page = response.urljoin(next_page)
            #yield scrapy.Request(next_page, callback=self.parse)

            # Unlike scrapy.Request, ``response.follow`` supports relative URLs directly - no
            # need to call urljoin. Note that ``response.follow`` just returns a Request
            # instance; you still have to yield this Request.
            yield response.follow(next_page, callback=self.parse)

        # OPTION 2
        # You can also pass a selector to ``response.follow`` instead of a string;
        # this selector should extract necessary attributes::    
        # for href in response.css('ul.pager a::attr(href)'):
        #   yield response.follow(href, callback=self.parse)
        # further shortcut 
        # for a in response.css('ul.pager a'):
        #   yield response.follow(a, callback=self.parse)

        # OPTION 3
        # To create multiple requests from an iterable, you can use
        # :meth:`response.follow_all <scrapy.http.TextResponse.follow_all>` instead::
        # anchors = response.css('ul.pager a')
        # yield from response.follow_all(anchors, callback=self.parse)
        # or, shortening it further::
        # yield from response.follow_all(css='ul.pager a', callback=self.parse)





