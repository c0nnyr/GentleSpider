# coding:utf-8

from BaseHandler import BaseItemHandler
import collections, time, logging
from MessagePostManager import MessagePostManager

class StatisticItemHandler(BaseItemHandler):

	LOG_DURATION = 60#每分钟记录一下

	POST_TEMPLATE = {
		'cd':
			{
				'HouseItem':'成都二手房{meta_district}-{meta_area}-{meta_price_level}: {count}',
				'CommunityItem':'成都小区{meta_district}-{meta_price_level}: {count}',
				'NewCommunityItem':'成都新盘{meta_district}: {count}',
				'DealItem':'成都成交{meta_district}-{meta_area}-{meta_price_level}: {count}',
			},
		'hz':
			{
				'HouseItem':'杭州二手房{meta_district}-{meta_area}-{meta_price_level}: {count}',
				'CommunityItem':'杭州小区{meta_district}-{meta_price_level}: {count}',
				'NewCommunityItem':'杭州新盘{meta_district}: {count}',
				'DealItem':'杭州成交{meta_district}-{meta_area}-{meta_price_level}: {count}',
			}
	}

	def __init__(self):
		super(StatisticItemHandler, self).__init__()
		self.statistic = collections.defaultdict(lambda:0)
		self.start_time = None
		self.last_log_time = None
		self.poster = MessagePostManager()
		self.cur_post_ind = 0
		self.template = None

	def open_spider(self):
		self.start_time = time.time()
		self.last_log_time = time.time()

	def close_spider(self):
		s0 = 'Total items:{}\n'.format(sum(self.statistic.itervalues()))
		s1 = '  '.join('{}:{}'.format(name, count) for name, count in self.statistic.iteritems())
		logging.info('StatisticItemHandler:' + s0 + s1)
		self._try_post(None)

	def handle(self, item, spider):
		self.statistic[item.__class__.__name__] += 1
		self._try_log()
		self._try_post(item)

	def _try_log(self):
		cur_time = time.time()
		if (cur_time - self.last_log_time) > self.LOG_DURATION:
			logging.info('Current statistic {}'.format(self.statistic))
			self.last_log_time = cur_time

	def _try_post(self, item):
		cur_time = time.time()
		post_ind = int((cur_time - self.start_time) / 3600 / 2)#没两个小时通知一次
		if post_ind > self.cur_post_ind or item is None:
			msg = ''
			try:
				if item:
					city = 'cd' if 'cd.lianjia' in item.url else 'hz'
					templates = self.POST_TEMPLATE[city]
					cls_name = item.__class__.__name__
					if cls_name not in templates:
						return
					self.template = templates[cls_name]
					msg = self.template.format(count=dict(self.statistic), **item.__dict__)
				else:
					if self.template:
						msg = self.template.format(count=dict(self.statistic), meta_district='END', meta_area='END', meta_price_level='END')
			except:
				if item:
					msg = 'Current find total items {}, current meta {}'.format(sum(self.statistic.itervalues()), item.__dict__, self.statistic)
				else:
					msg = 'Current find total items {}'.format(sum(self.statistic.itervalues()), self.statistic)
			title = 'Spider statistic'
			self.poster.post_immediatly(msg, title)
			self.cur_post_ind = post_ind


