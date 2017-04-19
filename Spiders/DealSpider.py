# coding:utf-8
from BaseLianjiaSpider import BaseLianjiaSpider
from Items import DealItem

class DealSpider(BaseLianjiaSpider):

	BASE_URL = 'http://cd.lianjia.com/chengjiao/{district}/{page}p{price_level}/'
	VALIDATE_XPATH = '/html/body/div[4]/div[1]'
	DISTRICTS = [ 'jinjiang', 'qingyang', 'wuhou', 'gaoxing7', 'chenghua', 'jinniu', \
	              'gaoxinxi1', 'pidou', 'tianfuxinqu', 'shuangliu', 'wenjiang', \
	              'longquanyi', 'xindou',]
	PRICE_LEVELS = [
		4,#80-100
		5,#100-150
		3,#60-80
		2,#40-60
		1,#<40
		6,#150-200
		7,#200-300
		8,#>300
	]

	metas = [{'price_level':price_level, 'district':district} for price_level in PRICE_LEVELS for district in DISTRICTS]
	start_urls = [BASE_URL.format(page='', district=meta['district'], price_level=meta['price_level']) for meta in metas]
	for start_url, meta in zip(start_urls, metas):
		meta['start_url'] = start_url
		meta['page'] = 1

	def parse(self, response):
		attr_map = {
			#attr xpath, re_filter
			'url':self.pack('div/div[1]/a/@href',),#这里不能再添加根了，不能/divxx or /li/div
			'id':self.pack('div/div[1]/a/@href', r'(?P<extract>\d+)'),
			'title':self.pack('div/div[1]/a/text()',),
			'description':self.pack('div/div[2]/div[1]/text()',),
			'description2':self.pack('div/div[3]/div[1]/text()',),
			'description3':self.pack('div/div[4]/div[1]/text()',),
		}
		for item in self._parse_multipage(response, DealItem, '/html/body/div[4]/div[1]/ul/li', attr_map, '/html/body/div[4]/div[1]/div[2]/div[1]/span'):
			yield item
