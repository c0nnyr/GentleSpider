# coding:utf-8
import cPickle
class Request(object):

	def __init__(self, url, method='get', data=None, meta=None, callback=None, **kwargs):
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

	def dumps(self):
		return cPickle.dumps(dict(url=self.url, data=self.data, meta=self.meta, method=self.method))

	def __str__(self):
		return '<Request {} {} {}>'.format(self._url, self._data, self._meta)
	__repr__ = __str__

