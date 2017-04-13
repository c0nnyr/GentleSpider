# coding:utf-8

from BaseHandler import BaseItemHandler
import collections, time, logging

class StatisticItemHandler(BaseItemHandler):

	def __init__(self):
		super(StatisticItemHandler, self).__init__()
		self.statistic = collections.defaultdict(0)
		self.start_time = None

	def open_spider(self):
		self.start_time = time.time()

	def close_spider(self):
		s0 = 'Total items:{}\n'.format(sum(self.statistic.itervalues()))
		s1 = '  '.join('{}:{}'.format(name, count) for name, count in self.statistic.iteritems())
		logging.info('StatisticItemHandler:' + s0 + s1)

	def handle(self, item):
		self.statistic[item.__class__.__name__] += 1

