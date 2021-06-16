import scrapy


class QuotesCSS(scrapy.Spider):
	name = "toscrape-xpath"
	start_urls = ['http://quotes.toscrape.com/']

	def parse(self, response):
		for quote in response.xpath('//div/quote'):
			yield {
				'text': quote.xpath('//span/text/text()').get(),
				'author': quote.xpath('//small/author/text()').get(),
				'tags': quote.xpath('//div/tags a/tag/text()').getall(),
			}
		yield from response.follow_all(css='ul.pager a', callback=self.parse)