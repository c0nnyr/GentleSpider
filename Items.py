# coding:utf-8
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, create_engine, and_, or_, DateTime

engine = create_engine('sqlite:///data.sqlite')
session_marker = sessionmaker(bind=engine)
session = session_marker()
Model = declarative_base(name='Model')

class LianJiaItem(object):
	IS_ITEM = True

	start_url = Column(Text())
	url = Column(Text(), primary_key=True)
	original_data = Column(Text())
	date = Column(Text())
	id = Column(Integer())
	request_response_id = Column(Integer())
	meta = Column(Text(), primary_key=True)
	page = Column(Integer())

	def __init__(self, **kwargs):
		super(LianJiaItem, self).__init__()
		assert all((k in kwargs) for k in ('start_url', 'url', 'original_data', 'id', 'request_response_id', 'meta')), "must contain keys 'start_url', 'url', 'original_data', 'id', 'meta'"
		self.date = self.get_today_str()
		for k, v in kwargs.iteritems():
			setattr(self, k, v)

	@staticmethod
	def get_today_str(delta=0):
		return (datetime.date.today() + datetime.timedelta(delta)).strftime('%y-%m-%d')

	@classmethod
	def check_page_crawled(cls, **kwargs):
		#检查是否曾经爬过这个页面. 对于一个单向队列的网页,用这个可以
		return session.query(cls).filter(and_(cls.start_url==kwargs.get('start_url'), cls.page==kwargs.get('page'), cls.date==cls.get_today_str())).count() > 0

	@classmethod
	def check_primary_existence(cls, item):
		return session.query(cls).filter(and_(cls.url == item.url, cls.date == item.date)).first()

class CommunityItem(LianJiaItem, Model):
	__tablename__ = 'community'

	title = Column(Text())
	count_on_sale = Column(Integer())
	price_per_sm = Column(Float())
	count_on_rent = Column(Integer())
	count_sold_90days = Column(Integer())
	district = Column(Text())
	bizcircle = Column(Text())
	year_built = Column(Integer())

class DealItem(LianJiaItem, Model):
	__tablename__ = 'deal'

	title = Column(Text())
	house_info = Column(Text())
	total_price = Column(Text())
	position_info = Column(Text())
	deal_platform = Column(Text())
	price_per_sm = Column(Text())
	deal_house_text = Column(Text())
	deal_cycle_txt = Column(Text())

	@classmethod
	def check_page_crawled(cls, **kwargs):
		return session.query(cls).filter(and_(cls.start_url==kwargs.get('start_url'), cls.page==kwargs.get('page'))).count() > 0
		#return session.query(cls).filter(and_(cls.start_url==kwargs.get('start_url'), cls.url==kwargs.get('url'))).count() > 0

class HouseItem(LianJiaItem, Model):
	__tablename__ = 'house'

	title = Column(Text())
	house_info_resblock = Column(Text())
	house_info = Column(Text())
	position_info_district = Column(Text())
	position_info = Column(Text())
	follow_info = Column(Text())
	total_price = Column(Text())
	price_per_sm = Column(Text())
	tag = Column(Text())

Model.metadata.create_all(engine)#类型建立后,才能这样建立表
