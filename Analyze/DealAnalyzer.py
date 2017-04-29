# coding:utf-8
#from Items import session as db
from BaseAnalyzer import BaseAnalyzer
import pprint, re
import GlobalMethod as M
from Spiders.DealSpider import DealSpider, DealItem

class DealAnalyzer(BaseAnalyzer):

	def run(self, **config):
		#self._handle_deal_cycle()
		#self._print_start_levels()
		self._handle_price()
		#self._handle_year()
		#self._handle_size()
		pass

	def _print_start_levels(self):
		for ind, start_url in enumerate(DealSpider.start_urls, 1):
			print ind, '/', len(DealSpider.start_urls), start_url

	def _handle_deal_cycle(self):
		results = db.query(DealItem.deal_cycle_txt, DealItem.total_price, DealItem.url).all()
		on_sale_pattern = re.compile(u'挂牌(?P<on_sale_price>\d+)')
		cycle_days_pattern = re.compile(u'成交周期(?P<cycle_days>\d*)')
		all_cycle_days = []
		all_on_sale_prices = []
		for result in results:
			txt = result[0]
			ret = re.search(on_sale_pattern, txt)
			on_sale_price = ret.group('on_sale_price') if ret else -1
			ret = re.search(cycle_days_pattern, txt)
			cycle_days = ret.group('cycle_days') if ret else -1
			all_cycle_days.append(float(cycle_days))
			all_on_sale_prices.append(float(on_sale_price))
		all_cycle_days = [min(days, 365) for days in all_cycle_days]
		#M.draw_hist(all_cycle_days, title=u'成交周期')
		#M.draw_hist(all_on_sale_prices, title=u'挂牌价格')

		valid_price_pair = [(on_sale_price - float(result[1]), on_sale_price, float(result[1]), result[2]) for on_sale_price, result in
							zip(all_on_sale_prices, results) if on_sale_price != -1]
		valid_price_pair = sorted(valid_price_pair, key=lambda x:x[0], reverse=True)
		#pprint.pprint(valid_price_pair)
		M.draw_hist(map(lambda x:min(max(x[0], -20), 20), valid_price_pair), title=u'成交差价')

	def _handle_price(self):
		results = db.query(DealItem.price_per_sm, DealItem.total_price).all()
		price_per_sm_lst = [float(result[0]) for result in results]
		M.draw_hist(price_per_sm_lst, title=u'成交单价')
		total_price_lst = [float(result[1]) for result in results]
		M.draw_hist(total_price_lst, title=u'成交总价')

	def _handle_year(self):
		results = db.query(DealItem.url, DealItem.position_info).all()
		year_patter = re.compile(u'(\d+)年')
		year_pairs = []
		for result in results:
			url, txt = result
			ret = re.search(year_patter, txt)
			year = int(ret.group(1)) if ret else 2020
			year_pairs.append((year, url))
		#pprint.pprint(sorted(year_pairs, key=lambda x:x[0], reverse=True))
		M.draw_hist(map(lambda x:x[0], year_pairs), title=u'房屋年限')

	def _handle_size(self):
		results = db.query(DealItem.url, DealItem.title).all()
		size_patter = re.compile(u'([0-9.]+)平米')
		size_pairs = []
		for result in results:
			url, txt = result
			ret = re.search(size_patter, txt)
			size = float(ret.group(1)) if ret else -1
			size_pairs.append((size, url))
		pprint.pprint(sorted(size_pairs, key=lambda x:x[0], reverse=False))
		M.draw_hist(map(lambda x:x[0], size_pairs), title=u'房屋大小')




