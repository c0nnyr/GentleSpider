# coding:utf-8
from BaseLianjiaSpider import BaseLianjiaSpider
import re
from Items import HouseItem
import GlobalMethod as M

class HouseSpider(BaseLianjiaSpider):
	BASE_URL = 'http://cd.lianjia.com/ershoufang/{district}/{page}co32p{price_level}/'#最新发布排序
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
			'url':self.pack('div[1]/div[contains(@class,"title")]/a/@href',),#这里不能再添加根了，不能/divxx or /li/div
			'id':self.pack('div[1]/div[contains(@class,"title")]/a/@href', r'(?P<extract>\d+)'),
			'title':self.pack('div[1]/div[contains(@class,"title")]/a/text()',),
			'house_info_resblock':self.pack('div[1]/div[contains(@class, "address")]/div[contains(@class, "houseInfo")]/a/text()', ),
			'house_info':self.pack('div[1]/div[contains(@class, "address")]/div[contains(@class, "houseInfo")]/text()', ),
			'position_info_district':self.pack('div[1]/div[contains(@class, "flood")]/div[contains(@class, "positionInfo")]/a/text()', ),
			'position_info':self.pack('div[1]/div[contains(@class, "flood")]/div[contains(@class, "positionInfo")]/text()', ),
			'follow_info':self.pack('div[1]/div[contains(@class, "followInfo")]/text()', ),
			'total_price':self.pack('div[1]/div[contains(@class, "priceInfo")]/div[contains(@class, "totalPrice")]/span/text()', ),
			'price_per_sm':self.pack('div[1]/div[contains(@class, "priceInfo")]/div[contains(@class, "unitPrice")]/span/text()', ),
			'tag':self.pack('div[1]/div[contains(@class, "tag")]/span/text()', ),
		}
		for item in self._parse_multipage(response, HouseItem, '/html/body/div[4]/div[1]/ul/li', attr_map, '/html/body/div[4]/div[1]/div[2]/h2/span/text()'):
			yield item

