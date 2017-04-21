# coding:utf-8
from Items import session as db
from Items import DealItem
from BaseAnalyzer import BaseAnalyzer

class DealAnalyzer(BaseAnalyzer):

	def run(self, **config):
		total_price = 0
		unit_prices = [float(item.price_per_sm) for item in db.query(DealItem).all()]
		print sorted(unit_prices, reverse=True)

