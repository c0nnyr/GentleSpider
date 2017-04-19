# coding:utf-8
from BaseLianjiaSpider import BaseLianjiaSpider
from Items import CommunityItem

class CommunitySpider(BaseLianjiaSpider):

	BASE_URL = 'http://cd.lianjia.com/xiaoqu/{page}p{price_level}/'
	VALIDATE_XPATH = '/html/body/div[4]/div[contains(@class,"leftContent")]'

	PRICE_LEVELS = [
		4,#1~1.5
		5,#1.5~2
		3,#0.8~1
		2,#0.5~0.8
		1,#<0.5
		6,#>2
	]

	metas = [{'price_level':price_level} for price_level in PRICE_LEVELS]
	start_urls = [BASE_URL.format(page='', price_level=meta['price_level']) for meta in metas]
	for start_url, meta in zip(start_urls, metas):
		meta['start_url'] = start_url
		meta['page'] = 1

	def parse(self, response):
		attr_map = {
			#attr xpath, re_filter
			'url':self.pack('div[2]/div[2]/a/@href',),#这里不能再添加根了，不能/divxx or /li/div
			'id':self.pack('div[2]/div[2]/a/@href', r'(?P<extract>\d+)'),
			'title':self.pack('div[1]/div[1]/a/text()',),
			'count_on_sale':self.pack('div[2]/div[2]/a/span/text()',),
			'price_per_sm':self.pack('div[2]/div[1]/div[1]/span/text()',),
			'count_on_rent':self.pack('div[1]/div[2]/a[2]/text()', r'(?P<extract>\d+)'),
			'count_sold_90days':self.pack('div[1]/div[2]/a[1]/text()', r'90\S+(?P<extract>\d+)'),
			'district':self.pack('div[1]/div[3]/a[1]/text()',),
			'bizcircle':self.pack('div[1]/div[3]/a[2]/text()',),
			'year_built':self.pack('div[1]/div[3]/text()',  r'(?P<extract>\d+)', '0'),
		}
		for item in self._parse_multipage(response, CommunityItem, '/html/body/div[4]/div[1]/ul/li', attr_map, '/html/body/div[4]/div[1]/div[2]/h2/span/text()'):
			yield item

