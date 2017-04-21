# coding:utf-8
from Items import session as db
from Items import DealItem
from BaseAnalyzer import BaseAnalyzer
import pprint, re

class DealAnalyzer(BaseAnalyzer):

	def run(self, **config):
		self._deal_cycle()

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


