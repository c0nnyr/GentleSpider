# coding:utf-8

class BaseItemHandler(object):
	def open_spider(self): pass
	def close_spider(self): pass
	def handle(self, item):
		print item.__dict__

class BaseRequestHandler(object):
	def open_spider(self): pass
	def close_spider(self): pass
	def handle(self, request): pass

class BaseResponseHandler(object):
	def open_spider(self): pass
	def close_spider(self): pass
	def handle(self, response): pass
