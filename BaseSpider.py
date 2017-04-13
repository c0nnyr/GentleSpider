# coding:utf-8
from Request import Request
import functools

class BaseSpider(object):

	def __init__(self, start_urls=()):
		self.start_urls = start_urls

	def get_start_requests(self):
		return [Request(start_url, callback=self.parse) for start_url in self.start_urls]

	def parse(self, response):
		pass

	def try_validate(self, response, callback):
		return []

	@staticmethod
	def pack(xpath, re_filter=None, default=0):
		return xpath, re_filter, default#这个辅助解包用好
