# coding:utf-8
from BaseHandler import BaseRequestHandler
import random, time, logging

class RandomWaitRequestHandler(BaseRequestHandler):

	def __init__(self):
		super(RandomWaitRequestHandler, self).__init__()
		self.has_handled = False

	def handle(self, request):
		if not self.has_handled:
			self.has_handled = True
			return
		delta = random.randint(5, 10)
		logging.info('waiting for {} seconds'.format(delta))
		time.sleep(delta)

