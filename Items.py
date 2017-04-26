# coding:utf-8
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, create_engine, and_, or_, DateTime
import GlobalMethod as M

class BaseItem(object):
	IS_ITEM = True
	_crawl_date = Column(DateTime())
	def __init__(self, **kwargs):
		super(BaseItem, self).__init__()
		assert all((k in kwargs) for k in ('_crawl_date',))
		for k, v in kwargs.iteritems():
			setattr(self, k, v)

	def check_existence(self):
		return False

#class LianJiaItem(object):
#	IS_ITEM = True
#
#	start_url = Column(Text())
#	url = Column(Text(), primary_key=True)
#	original_data = Column(Text())
#	date = Column(Text())
#	id = Column(Integer())
#	request_response_id = Column(Integer())
#	meta = Column(Text(), primary_key=True)
#	page = Column(Integer())
#
#	def __init__(self, **kwargs):
#		super(LianJiaItem, self).__init__()
#		assert all((k in kwargs) for k in ('start_url', 'url', 'original_data', 'id', 'request_response_id', 'meta')), "must contain keys 'start_url', 'url', 'original_data', 'id', 'meta'"
#		self.date = self.get_today_str()
#		for k, v in kwargs.iteritems():
#			setattr(self, k, v)
#
#	@staticmethod
#	def get_today_str(delta=0):
#		return (datetime.date.today() + datetime.timedelta(delta)).strftime('%y-%m-%d')
#
#	@classmethod
#	def check_page_crawled(cls, **kwargs):
#		#检查是否曾经爬过这个页面. 对于一个单向队列的网页,用这个可以
#		return session.query(cls).filter(and_(cls.start_url==kwargs.get('start_url'), cls.page==kwargs.get('page'), cls.date==cls.get_today_str())).count() > 0
#
#	@classmethod
#	def check_primary_existence(cls, item):
#		return session.query(cls).filter(and_(cls.url == item.url, cls.date == item.date)).first()
#
#class CommunityItem(LianJiaItem, Model):
#	__tablename__ = 'community'
#
#	title = Column(Text())
#	count_on_sale = Column(Integer())
#	unit_price = Column(Float())
#	count_on_rent = Column(Integer())
#	count_sold_90days = Column(Integer())
#	district = Column(Text())
#	bizcircle = Column(Text())
#	year_built = Column(Integer())

_engine, _session, _Model = M.create_db_engine('deal')
class DealItem(BaseItem, _Model):
	__tablename__ = 'deal'
	db = _session

	meta_district = Column(Text(), primary_key=True)
	meta_area = Column(Text(), primary_key=True)
	meta_price_level = Column(Text(), primary_key=True)
	meta_start_url = Column(Text(), primary_key=True)
	meta_direction = Column(Text(), primary_key=True)

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

	def check_already_stored(self):
		cls = self.__class__
		return cls.db.query(cls).filter(meta_district=self.meta_district,
										meta_area=self.meta_area,
										meta_price_level=self.meta_price_level,
										meta_start_url=self.meta_start_url,
										meta_direction=self.meta_direction,
										url=self.url).count() > 0

	def __str__(self):
		return '<{}> {} {}'.format(self.__class__.__name__, self.meta_start_url, self.url)
	__repr__ = __str__

_Model.metadata.create_all(_engine)#类型建立后,才能这样建立表

#class HouseItem(LianJiaItem, Model):
#	__tablename__ = 'house'
#
#	title = Column(Text())
#	house_info_resblock = Column(Text())
#	house_info = Column(Text())
#	position_info_district = Column(Text())
#	position_info = Column(Text())
#	follow_info = Column(Text())
#	total_price = Column(Text())
#	unit_price = Column(Text())
#	tag = Column(Text())
#
#class BookItem(BaseItem, Model):
#	IS_ITEM = True
#	__tablename__ = 'book'
#
#	url = Column(Text(), primary_key=True)
#	id = Column(Text())
#	title = Column(Text())
#	sub_title = Column(Text())
#	pub = Column(Text())
#	rating_nums = Column(Text())
#	rating_count = Column(Text())
#	description = Column(Text())
#	book_price = Column(Text())
#	img_url = Column(Text())
#
#	def __init__(self, **kwargs):
#		super(BookItem, self).__init__()
#		for k, v in kwargs.iteritems():
#			if hasattr(self, k):
#				setattr(self, k, v)
#
#	def __str__(self):
#		return '<BookItem>url {}, meta {}'.format(self.url, self._meta)
#
#Model.metadata.create_all(engine)#类型建立后,才能这样建立表
