# coding:utf-8
from BaseLianjiaSpider import BaseLianjiaSpider
import re
from BaseItem import BaseItem
import GlobalMethod as M
from sqlalchemy import Column, Text, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base

_Model = declarative_base(name='house')
class HouseItem(BaseItem, _Model):
	__tablename__ = 'house'

	_crawl_date = Column(DateTime())
	meta_district = Column(Text(), primary_key=True)
	meta_area = Column(Text(), primary_key=True)
	meta_price_level = Column(Text(), primary_key=True)
	meta_start_url = Column(Text())

	url = Column(Text(), primary_key=True)
	house_id = Column(Text())

	title = Column(Text())
	house_info_resblock = Column(Text())
	house_info = Column(Text())
	position_info_district = Column(Text())
	position_info = Column(Text())
	tag = Column(Text())

	def __str__(self):
		return '<{}> {} {}'.format(self.__class__.__name__, self.meta_start_url, self.url)
	__repr__ = __str__

class HouseStateItem(BaseItem, _Model):
	__tablename__ = 'house_state'

	meta_start_date = Column(Date(), primary_key=True)
	meta_district = Column(Text(), primary_key=True)
	meta_area = Column(Text(), primary_key=True)
	meta_price_level = Column(Text(), primary_key=True)
	url = Column(Text(), primary_key=True)

	follow_info = Column(Text())
	total_price = Column(Text())
	unit_price = Column(Text())

	def __str__(self):
		return '<{}> {}'.format(self.__class__.__name__, self.url)
	__repr__ = __str__
class HouseSpider(BaseLianjiaSpider):
	START_FROM_LIKE_URL = 'gongshu/a8p1'

	VALIDATE_XPATH = '/html/body/div[4]/div[contains(@class,"leftContent")]'

	BASIC_DATA = {
		'cd':{
			'BASE_URL':'http://cd.lianjia.com/ershoufang/{district}/{page}co32a{area}p{price_level}/',#最新发布排序
			'DISTRICTS':[ 'jinjiang', 'qingyang', 'wuhou', 'gaoxing7', 'chenghua', 'jinniu', \
						  'gaoxinxi1', 'pidou', 'tianfuxinqu', 'shuangliu', 'wenjiang', \
						  'longquanyi', 'xindou',],
			'PRICE_LEVELS':[
				8,#>300
				7,#200-300
				6,#150-200
				5,#100-150
				4,#80-100
				3,#60-80
				2,#40-60
				1,#<40
			],
			'AREAS':[
				8,#>200
				7,#150~200
				6,#130~150
				5,#110~130
				4,#90~110
				3,#70~90
				2,#50~70
				1,#<50
			]
		},
		'hz':{
			'BASE_URL':'http://hz.lianjia.com/ershoufang/{district}/{page}a{area}p{price_level}/',
			'DISTRICTS':['xihu', 'xiacheng', 'jianggan', 'gongshu', 'shangcheng', 'binjiang', \
						 'yuhang', 'xiaoshan', 'xiasha'],
			'PRICE_LEVELS':[
				6,#>500
				5,#300-500
				4,#200-300
				3,#150-200
				2,#100-150
				1,#<100
			],
			'AREAS':[
				8,#>200
				7,#150~200
				6,#130~150
				5,#110~130
				4,#90~110
				3,#70~90
				2,#50~70
				1,#<50
			]
		}
	}

	def __init__(self, city):
		super(HouseSpider, self).__init__()
		self.session = M.create_engine('house', _Model, prefix='data', suffix=city)
		basic_data = self.BASIC_DATA.get(city)
		if basic_data:
			self.metas = [{'price_level':price_level, 'district':district, 'area':area, }
						  for price_level in basic_data['PRICE_LEVELS']
						  for district in basic_data['DISTRICTS']
						  for area in basic_data['AREAS']]
			self.BASE_URL = basic_data['BASE_URL']
			self.start_urls = M.fill_meta_extract_start_urls(self.BASE_URL, self.metas)
		else:
			raise Exception('not supported city')


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

