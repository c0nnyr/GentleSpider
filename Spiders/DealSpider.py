# coding:utf-8
from BaseLianjiaSpider import BaseLianjiaSpider
from Items import DealItem

class DealSpider(BaseLianjiaSpider):

	CHECK_HAS_CRAWLED_PAGE = True

	BASE_URL = 'http://cd.lianjia.com/chengjiao/{district}/{page}p{price_level}/'
	VALIDATE_XPATH = '/html/body/div[4]/div[contains(@class,"leftContent")]'
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
	start_urls = [BASE_URL.format(page='', **meta) for meta in metas]
	for start_url, meta in zip(start_urls, metas):
		meta['start_url'] = start_url
		meta['page'] = 1

	def parse(self, response):
		attr_map = {
			#attr xpath, re_filter
			'url':self.pack('div/div[1]/a/@href',),#这里不能再添加根了，不能/divxx or /li/div
			'id':self.pack('div/div[1]/a/@href', r'chengjiao/(?P<extract>\S+)\.'),
			'date':self.pack('div/div/div[contains(@class, "dealDate")]/text()',),
			'title':self.pack('div/div[1]/a/text()',),
			'house_info':self.pack('div/div/div[contains(@class, "houseInfo")]/text()',),
			'total_price':self.pack('div/div/div[contains(@class, "totalPrice")]/span/text()',),
			'position_info':self.pack('div/div/div[contains(@class, "positionInfo")]/text()',),
			'deal_platform':self.pack('div/div/div[contains(@class, "source")]/text()',),
			'price_per_sm':self.pack('div/div/div[contains(@class, "unitPrice")]/span/text()',),
			'deal_house_text':self.pack('div/div/span[contains(@class, "dealHouseTxt")]/span/text()',),
			'deal_cycle_txt':self.pack('div/div/span[contains(@class, "dealCycleTxt")]/span/text()',),
		}
		for item in self._parse_multipage(response, DealItem, '/html/body/div[4]/div[1]/ul/li', attr_map, '/html/body/div[4]/div[1]/div[2]/div[1]/span/text()'):
			yield item
