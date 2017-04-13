# coding:utf-8
from Request import Request
import functools

class BaseSpider(object):
	USE_CACHE = False

	def __init__(self, start_urls=()):
		self.start_urls = start_urls

	def get_start_requests(self):
		return [Request(start_url, use_cache=self.USE_CACHE) for start_url in self.start_urls]

	def parse(self, response):
		pass

	def try_validate(self, response, callback):
		return []

	def is_valid_response(self, response):
		return True
