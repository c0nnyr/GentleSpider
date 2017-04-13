# coding:utf-8
from BaseHandler import BaseRequestHandler
import random, time, logging

class RandomWaitRequestHandler(BaseRequestHandler):

	def handle(self, request):
		delta = random.randint(5, 10)
		logging.info('waiting for {} seconds'.format(delta))
		time.sleep(delta)

