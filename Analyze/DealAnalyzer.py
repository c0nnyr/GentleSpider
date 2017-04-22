# coding:utf-8
from Items import session as db
from Items import DealItem
from BaseAnalyzer import BaseAnalyzer
import pprint, re

class DealAnalyzer(BaseAnalyzer):

	def run(self, **config):
		total_count = db.query(DealItem).count()
		for ind, item in enumerate(db.query(DealItem).all()):
			db.merge(item)
			db.commit()
			print ind, '/', total_count
		#self._deal_cycle()
		#self._deal_page()

	def _deal_page(self):
		query = db.query(DealItem).filter(DealItem.id == 106100214277)
		item = query.first()
		print query
		print item.__dict__
		print item.id, item.start_url, item.url, item.page, item.request_response_id, item.title
		#total_count = 0
		#for page in xrange(101):
		#	count = db.query(DealItem).filter(DealItem.page==page).count()
		#	response_ids = sorted([item.request_response_id for item in db.query(DealItem).filter(DealItem.page==page).all()])
		#	if len(response_ids) != count:
		#		print 'not equal', page
		#	print response_ids
		#	total_count += count
		#	print page, count
		#print total_count
		#print db.query(DealItem).count()
		#items = db.query(DealItem).filter(DealItem.page==100).all()
		#for ind, item in enumerate(items):
		#	print ind, item.start_url

	def _deal_cycle(self):
		total_price = 0
		on_sale_pattern = re.compile(u'挂牌(?P<on_sale_price>\d+)')
		cycle_days_pattern = re.compile(u'成交周期(?P<cycle_days>\d*)')
		all_cycle_days = []
		for item in db.query(DealItem).all():
			txt = item.deal_cycle_txt
			results = re.search(on_sale_pattern, txt)
			on_sale_price = results.group('on_sale_price') if results else -1
			results = re.search(cycle_days_pattern, txt)
			cycle_days = results.group('cycle_days') if results else -1
			all_cycle_days.append(cycle_days)
			print on_sale_price, cycle_days, txt
		print all_cycle_days


