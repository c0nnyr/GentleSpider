# coding:utf-8
from BaseHandler import BaseRequestHandler
import random, time, logging

class RandomWaitRequestHandler(BaseRequestHandler):

	def __init__(self):
		super(RandomWaitRequestHandler, self).__init__()
		self.has_handled = False

	def handle(self, request, spider):
		if not self.has_handled:
			self.has_handled = True
			return
		delta = random.randint(1, 3)
		logging.info('waiting for {} seconds'.format(delta))
		time.sleep(delta)

	def need_skip_when_use_cache(self, is_last_request_using_cache):
		return is_last_request_using_cache

