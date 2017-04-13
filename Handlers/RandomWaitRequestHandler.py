# coding:utf-8
from BaseHandler import BaseRequestHandler
import random, time

class RandomWaitRequestHandler(BaseRequestHandler):

	def handle(self, request):
		delta = random.randint(5, 10)
		time.sleep(delta)

