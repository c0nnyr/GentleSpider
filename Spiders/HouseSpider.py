# coding:utf-8
from BaseLianjiaSpider import BaseLianjiaSpider
import re
from Items import HouseItem, HouseStateItem
import GlobalMethod as M

class HouseSpider(BaseLianjiaSpider):
	BASE_URL = 'http://cd.lianjia.com/ershoufang/{district}/{page}co32a{area}p{price_level}/'#最新发布排序
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
	AREAS = [
		1,#<50
		2,#50~70
		3,#70~90
		4,#90~110
		5,#110~130
		6,#130~150
		7,#150~200
		8,#>200
	]
	metas = [{'price_level':price_level, 'district':district, 'area':area, }
			 for price_level in PRICE_LEVELS
			 for district in DISTRICTS
			 for area in AREAS]
	start_urls = M.fill_meta_extract_start_urls(BASE_URL, metas)

	def parse(self, response):
		attr_map = {
			#attr xpath, re_filter
			'url':dict(xpath='div[1]/div[contains(@class,"title")]/a/@href',),#这里不能再添加根了，不能/divxx or /li/div
			'house_id':dict(xpath='div[1]/div[contains(@class,"title")]/a/@href', re_filter=r'ershoufang/(?P<extract>\S+)\.'),
			'title':dict(xpath='div[1]/div[contains(@class,"title")]/a/text()',),
			'house_info_resblock':dict(xpath='div[1]/div[contains(@class, "address")]/div[contains(@class, "houseInfo")]/a/text()', ),
			'house_info':dict(xpath='div[1]/div[contains(@class, "address")]/div[contains(@class, "houseInfo")]/text()', ),
			'position_info_district':dict(xpath='div[1]/div[contains(@class, "flood")]/div[contains(@class, "positionInfo")]/a/text()', ),
			'position_info':dict(xpath='div[1]/div[contains(@class, "flood")]/div[contains(@class, "positionInfo")]/text()', ),
			'tag':dict(xpath='div[1]/div[contains(@class, "tag")]/span/text()', ),
		}
		for item in self._parse_multipage(response, HouseItem, '/html/body/div[4]/div[1]/ul/li', attr_map, \
										  '/html/body/div[4]/div[1]/div[2]/h2/span/text()', \
										  ('district', 'price_level', 'area', 'start_url')):
			yield item
		attr_map = {
			#attr xpath, re_filter
			'url':dict(xpath='div[1]/div[contains(@class,"title")]/a/@href',),#这里不能再添加根了，不能/divxx or /li/div
			'follow_info':dict(xpath='div[1]/div[contains(@class, "followInfo")]/text()', ),
			'total_price':dict(xpath='div[1]/div[contains(@class, "priceInfo")]/div[contains(@class, "totalPrice")]/span/text()', ),
			'unit_price':dict(xpath='div[1]/div[contains(@class, "priceInfo")]/div[contains(@class, "unitPrice")]/span/text()', ),
		}
		for item in self._parse_items(response, '/html/body/div[4]/div[1]/ul/li', attr_map, HouseStateItem, \
										  ('district', 'price_level', 'area', 'start_date')):
			yield item

