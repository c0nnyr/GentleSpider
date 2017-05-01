# coding:utf-8

class BaseItemHandler(object):
	def open_spider(self): pass
	def close_spider(self): pass
	def handle(self, item, spider):
		print item.__dict__

class BaseRequestHandler(object):
	def open_spider(self): pass
	def close_spider(self): pass
	def handle(self, request, spider): pass
	def need_skip_when_use_cache(self, is_last_request_using_cache):pass

class BaseResponseHandler(object):
	def open_spider(self): pass
	def close_spider(self): pass
	def handle(self, response, spider): pass
