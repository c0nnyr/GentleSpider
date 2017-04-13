# coding:utf-8
from sqlalchemy import Column, Integer, String, Text, Float, create_engine, and_, or_
import SqlDBHelper as db
import datetime

class LianJiaItem(object):
	IS_ITEM = True

	start_url = Column(Text())
	url = Column(Text())
	original_data = Column(Text())
	date = Column(Text(), primary_key=True)
	id = Column(Integer(), primary_key=True)

	def __init__(self, **kwargs):
		super(LianJiaItem, self).__init__()
		assert all((k in kwargs) for k in ('start_url', 'url', 'original_data', 'id')), "must contain keys 'start_url', 'url', 'original_data', 'id'"
		self.date = self.get_today_str()
		for k, v in kwargs.iteritems():
			setattr(self, k, v)

	@staticmethod
	def get_today_str(delta=0):
		return (datetime.date.today() + datetime.timedelta(delta)).strftime('%y-%m-%d')

class CommunityItem(LianJiaItem, db.Model):
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

class DealItem(LianJiaItem, db.Model):
	__tablename__ = 'deal_item'

	title = Column(Text())
	total_price = Column(Text())
	price_per_sm = Column(Text())
	deal_by = Column(Text())
	description = Column(Text())
	description2 = Column(Text())
	district_description = Column(Text())
	price_when_on = Column(Text())
	days_when_sale = Column(Text())
	page = Column(Integer())

db.Model.metadata.create_all(db.engine)#类型建立后,才能这样建立表
