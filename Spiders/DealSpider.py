# coding:utf-8
from BaseLianjiaSpider import BaseLianjiaSpider
import GlobalMethod as M
from BaseItem import BaseItem
from sqlalchemy import Column, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

_Model = declarative_base(name='deal')
class DealItem(BaseItem, _Model):
	__tablename__ = 'deal'

	_crawl_date = Column(DateTime())
	meta_district = Column(Text(), primary_key=True)
	meta_area = Column(Text(), primary_key=True)
	meta_price_level = Column(Text(), primary_key=True)
	meta_start_url = Column(Text())

	url = Column(Text(), primary_key=True)
	deal_id = Column(Text())
	deal_date = Column(Text())
	title = Column(Text())
	house_info = Column(Text())
	total_price = Column(Text())
	position_info = Column(Text())
	deal_platform = Column(Text())
	unit_price = Column(Text())
	deal_house_text = Column(Text())
	deal_cycle_txt = Column(Text())

	def check_existence(self, session):
		cls = self.__class__
		return session.query(cls).filter_by(meta_district=self.meta_district,
										   meta_area=self.meta_area,
										   meta_price_level=self.meta_price_level,
										   url=self.url).count() > 0

	def __str__(self):
		return '<{}> {} {}'.format(self.__class__.__name__, self.meta_start_url, self.url)
	__repr__ = __str__

class DealSpider(BaseLianjiaSpider):

	VALIDATE_XPATH = '/html/body/div[4]/div[contains(@class,"leftContent")]'

	BASIC_DATA = {
		'cd':{
			'BASE_URL':'http://cd.lianjia.com/chengjiao/{district}/{page}co32a{area}p{price_level}/',#最新发布排序
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
			'BASE_URL':'http://hz.lianjia.com/chengjiao/{district}/{page}a{area}p{price_level}/',
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
		super(DealSpider, self).__init__()
		self.session = M.create_engine('deal', _Model, prefix='data', suffix=city)
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
			'url':dict(xpath='div/div[1]/a/@href',),#这里不能再添加根了，不能/divxx or /li/div
			'deal_id':dict(xpath='div/div[1]/a/@href', re_filter=r'chengjiao/(?P<extract>\S+)\.'),
			'deal_date':dict(xpath='div/div/div[contains(@class, "dealDate")]/text()',),
			'title':dict(xpath='div/div[1]/a/text()',),
			'house_info':dict(xpath='div/div/div[contains(@class, "houseInfo")]/text()',),
			'total_price':dict(xpath='div/div/div[contains(@class, "totalPrice")]/span/text()',),
			'position_info':dict(xpath='div/div/div[contains(@class, "positionInfo")]/text()',),
			'deal_platform':dict(xpath='div/div/div[contains(@class, "source")]/text()',),
			'unit_price':dict(xpath='div/div/div[contains(@class, "unitPrice")]/span/text()',),
			'deal_house_text':dict(xpath='div/div/span[contains(@class, "dealHouseTxt")]/span/text()',),
			'deal_cycle_txt':dict(xpath='div/div/span[contains(@class, "dealCycleTxt")]/span/text()',),
		}
		for item in self._parse_multipage(response, DealItem, '/html/body/div[4]/div[1]/ul/li', attr_map,
										  '/html/body/div[4]/div[1]/div[2]/div[1]/span/text()',
										  ('district', 'price_level', 'area', 'start_url')):
			yield item
