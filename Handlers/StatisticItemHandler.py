# coding:utf-8

from BaseHandler import BaseItemHandler
import collections, time, logging

class StatisticItemHandler(BaseItemHandler):

	LOG_DURATION = 60#每分钟记录一下

	def __init__(self):
		super(StatisticItemHandler, self).__init__()
		self.statistic = collections.defaultdict(lambda:0)
		self.start_time = None
		self.last_log_time = None

	def open_spider(self):
		self.start_time = time.time()
		self.last_log_time = time.time()

	def close_spider(self):
		s0 = 'Total items:{}\n'.format(sum(self.statistic.itervalues()))
		s1 = '  '.join('{}:{}'.format(name, count) for name, count in self.statistic.iteritems())
		logging.info('StatisticItemHandler:' + s0 + s1)

	def handle(self, item):
		self.statistic[item.__class__.__name__] += 1
		self._try_log()

	def _try_log(self):
		cur_time = time.time()
		if (cur_time - self.last_log_time) > self.LOG_DURATION:
			logging.info('Current statistic {}'.format(self.statistic))
			self.last_log_time = cur_time


