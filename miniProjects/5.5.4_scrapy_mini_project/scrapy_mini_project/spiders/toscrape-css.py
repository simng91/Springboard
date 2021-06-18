import scrapy


class QuotesCSS(scrapy.Spider):
	name = "toscrape-css"
	start_urls = ['http://quotes.toscrape.com/']

	def parse(self, response):
		for quote in response.css('div.quote'):
			yield {
				'text': quote.css('span.text::text').get(),
				'author': quote.css('small.author::text').get(),
				'tags': quote.css('div.tags a.tag::text').getall(),
			}
		yield from response.follow_all(css='ul.pager a', callback=self.parse)