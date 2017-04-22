# coding:utf-8
from Items import session as db
from Items import DealItem
from BaseAnalyzer import BaseAnalyzer
import pprint, re
import GlobalMethod as M
from Spiders.DealSpider import DealSpider

class DealAnalyzer(BaseAnalyzer):

	def run(self, **config):
		self._deal_cycle()
		#self._deal_page()
		self._print_start_levels()
		pass

	def _print_start_levels(self):
		for ind, start_url in enumerate(DealSpider.start_urls, 1):
			print ind, '/', len(DealSpider.start_urls), start_url

	def _deal_cycle(self):
		total_price = 0
		on_sale_pattern = re.compile(u'挂牌(?P<on_sale_price>\d+)')
		cycle_days_pattern = re.compile(u'成交周期(?P<cycle_days>\d*)')
		all_cycle_days = []
		all_on_sale_prices = []
		for item in db.query(DealItem).all():
			txt = item.deal_cycle_txt
			results = re.search(on_sale_pattern, txt)
			on_sale_price = results.group('on_sale_price') if results else -1
			results = re.search(cycle_days_pattern, txt)
			cycle_days = results.group('cycle_days') if results else -1
			all_cycle_days.append(int(cycle_days))
			all_on_sale_prices.append(int(on_sale_price))
		all_cycle_days = [min(days, 365) for days in all_cycle_days]

		import numpy as np
		import matplotlib.mlab as mlab
		import matplotlib.pyplot as plt

		np.random.seed(0)

		# example data
		#mu = 100  # mean of distribution
		#sigma = 15  # standard deviation of distribution
		#x = mu + sigma * np.random.randn(437)

		num_bins = 50

		fig, ax = plt.subplots()

		# the histogram of the data
		n, bins, patches = ax.hist(all_on_sale_prices, num_bins, normed=1)

		# add a 'best fit' line
		#y = mlab.normpdf(bins, mu, sigma)
		#ax.plot(bins, y, '--')
		ax.set_xlabel('Smarts')
		ax.set_ylabel('Probability density')
		ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

		# Tweak spacing to prevent clipping of ylabel
		fig.tight_layout()
		plt.show()



