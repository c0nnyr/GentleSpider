# coding:utf-8
from BaseLianjiaSpider import BaseLianjiaSpider
import GlobalMethod as M
from BaseItem import BaseItem
from sqlalchemy import Column, Text, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from Request import Request

_Model = declarative_base(name='new_community')
class NewCommunityItem(BaseItem, _Model):
	__tablename__ = 'new_community'

	_crawl_date = Column(DateTime())
	meta_district = Column(Text(), primary_key=True)
	meta_start_url = Column(Text())

	url = Column(Text(), primary_key=True)

	title = Column(Text())
	bizcircle = Column(Text())
	house_rooms = Column(Text())
	house_size = Column(Text())
	tag = Column(Text())

	def __str__(self):
		return '<{}> {} {}'.format(self.__class__.__name__, self.meta_start_url, self.url)
	__repr__ = __str__

#class NewCommunityDetailItem(BaseItem, _Model):
#	__tablename__ = 'new_community_detail'
#
#	_crawl_date = Column(DateTime())
#	meta_district = Column(Text(), primary_key=True)
#	meta_start_url = Column(Text())
#
#	url = Column(Text(), primary_key=True)
#
#	title = Column(Text())
#	bizcircle = Column(Text())
#	house_rooms = Column(Text())
#	house_size = Column(Text())
#	tag = Column(Text())
#
#	def __str__(self):
#		return '<{}> {} {}'.format(self.__class__.__name__, self.meta_start_url, self.url)
#	__repr__ = __str__

class NewCommunityStateItem(BaseItem, _Model):
	__tablename__ = 'new_community_state'

	meta_start_date = Column(Date(), primary_key=True)
	meta_district = Column(Text(), primary_key=True)
	url = Column(Text(), primary_key=True)

	unit_price = Column(Text())
	tag = Column(Text())

	def __str__(self):
		return '<{}> {}'.format(self.__class__.__name__, self.url)
	__repr__ = __str__

class NewCommunitySpider(BaseLianjiaSpider):
	VALIDATE_XPATH = '/html/body/div[5]/div'
	BASIC_DATA = {
		'cd':{
			'BASE_URL':'http://cd.lianjia.com/loupan/{district}/{page}/',
			'DISTRICTS':[ 'jinjiang', 'qingyang', 'wuhou', 'gaoxin7', 'chenghua', 'jinniu', \
						  'gaoxinxi1', 'pidou', 'tianfuxinqu', 'shuangliu', 'wenjiang', \
						  'longquanyi', 'xindou',],
		},
		'hz':{
			'BASE_URL':'http://hz.lianjia.com/loupan/{district}/{page}/',
			'DISTRICTS':['xihu', 'xiacheng', 'jianggan', 'gongshu', 'shangcheng', 'binjiang', \
						 'yuhang', 'xiaoshan', 'xiasha'],
		}
	}

	MAX_COUNT_PER_PAGE = 10

	def __init__(self, city='cd'):
		super(NewCommunitySpider, self).__init__()
		self.session = M.create_engine('new_community', _Model, prefix='data', suffix=city)
		basic_data = self.BASIC_DATA.get(city)
		if basic_data:
			self.metas = [{'district':district, }
						  for district in basic_data['DISTRICTS']]
			self.BASE_URL = basic_data['BASE_URL']
			self.start_urls = M.fill_meta_extract_start_urls(self.BASE_URL, self.metas)
		else:
			raise Exception('not supported city')

	def parse(self, response):
		attr_map = {
			#attr xpath, re_filter
			'url':dict(xpath='div[@class="info-panel"]/div[@class="col-1"]/h2/a/@href',),#这里不能再添加根了，不能/divxx or /li/div
			'title':dict(xpath='div[@class="info-panel"]/div[@class="col-1"]/h2/a/text()',),
			'bizcircle':dict(xpath='div[@class="info-panel"]/div[@class="col-1"]/div[@class="where"]/span/text()',),
			'house_rooms':dict(xpath='div[@class="info-panel"]/div[@class="col-1"]/div[@class="area"]/text()',),
			'house_size':dict(xpath='div[@class="info-panel"]/div[@class="col-1"]/div[@class="area"]/span/text()',),
			'tag':dict(xpath='div[@class="info-panel"]/div[@class="col-1"]/div[@class="type"]/span/text()',),
		}
		for item in self._parse_multipage(response, NewCommunityItem, '//*[@id="house-lst"]/li', attr_map, '//*[@id="findCount"]/text()', ('district', 'start_url', )):
			yield item
			#meta = response.meta.copy()
			#meta['validate_xpath'] = '//*[@id="house-details"]'
			#yield Request('http://cd.fang.lianjia.com/loupan' + item.url + 'xiangqing', callback='_parse_detail', meta=meta)

		attr_map = {
			'url':dict(xpath='div[@class="info-panel"]/div[@class="col-1"]/h2/a/@href',),#这里不能再添加根了，不能/divxx or /li/div
			'unit_price':dict(xpath='div[@class="info-panel"]/div[@class="col-2"]/div[@class="price"]/div[@class="average"]/span/text()',),
			'tag':dict(xpath='div[@class="info-panel"]/div[@class="col-1"]/div[@class="type"]/span/text()',),
		}

		for item in self._parse_items(response, '//*[@id="house-lst"]/li', attr_map, NewCommunityStateItem, \
									  ('district', 'start_date')):
			yield item
#
#	def _parse_detail(self, response):
#		raise NotImplementedError
#		attr_map = {
#			'tag':dict(xpath='div[@class="info-panel"]/div[@class="col-1"]/div[@class="type"]/span/text()',),
#		}
#		item = self._parse_item(response, attr_map, NewCommunityStateItem, \
#									  ('district', 'start_date'))
#		if item:
#			yield item

