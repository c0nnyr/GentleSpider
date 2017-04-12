# coding:utf-8
class Request(object):
	def __init__(self, url, method='get', data=None, meta=None, callback=None):
		self._url = url
		self._data = data or {}
		self._meta = meta or {}
		self._method = method
		self._callback = callback

	@property
	def url(self):
		return self._url
	@property
	def data(self):
		return self._data
	@property
	def meta(self):
		return self._meta
	@property
	def method(self):
		return self._method
	@property
	def callback(self):
		return self._callback
