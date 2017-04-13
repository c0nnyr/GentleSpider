# coding:utf-8

class BaseItemHandler(object):
	def handle(self, item):
		print item.__dict__

class BaseRequestHandler(object):
	def handle(self, request):
		pass

class BaseResponseHandler(object):
	def handle(self, response):
		pass
