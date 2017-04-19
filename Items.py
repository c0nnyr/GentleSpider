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
	url = Column(Text())
	original_data = Column(Text())
	date = Column(Text(), primary_key=True)
	id = Column(Integer(), primary_key=True)
	request_response_id = Column(Integer())

	def __init__(self, **kwargs):
		super(LianJiaItem, self).__init__()
		assert all((k in kwargs) for k in ('start_url', 'url', 'original_data', 'id', 'request_response_id')), "must contain keys 'start_url', 'url', 'original_data', 'id'"
		self.date = self.get_today_str()
		for k, v in kwargs.iteritems():
			setattr(self, k, v)

	@staticmethod
	def get_today_str(delta=0):
		return (datetime.date.today() + datetime.timedelta(delta)).strftime('%y-%m-%d')

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
	page = Column(Integer())

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

	page = Column(Integer())

class HouseItem(LianJiaItem, Model):
	__tablename__ = 'house'

Model.metadata.create_all(engine)#类型建立后,才能这样建立表
