# coding:utf-8
from BaseObject import BaseObject
from BaseHandler import BaseItemHandler, BaseRequestHandler, BaseResponseHandler
from BaseSpider import BaseSpider
from Request import Request
import GlobalMethod as M
import itertools, logging
from SqlDBHelper import session as db
from SqlDBHelper import ProxyItem, RequestResponseMap

class Dispatcher(BaseObject):

	def __init__(self):
		super(Dispatcher, self).__init__()
		self._network_service = None
		self._item_handler_list = []
		self._request_handler_list = []
		self._response_handler_list = []

	def run(self, *spiders):
		for handler in itertools.chain(self._item_handler_list, self._response_handler_list, self._request_handler_list):
			handler.open_spider()
		for spider in spiders:
			assert isinstance(spider, BaseSpider), 'spider must be instance of BaseSpider'
			request_or_items = spider.get_start_requests()
			self._run(M.arg_to_iter(request_or_items), spider)
		for handler in itertools.chain(self._item_handler_list, self._response_handler_list, self._request_handler_list):
			handler.close_spider()

	def _run(self, request_or_items, spider):
		for request_or_item in request_or_items:
			if M.is_item(request_or_item):
				logging.info('Find item {}'.format(request_or_item.__dict__))
				for handler in self._item_handler_list:
					try:
						handler.handle(request_or_item)
					except Exception as ex:
						logging.info('Exception {} happens when using {}'.format(ex, handler))
			elif isinstance(request_or_item, Request):
				for handler in self._request_handler_list:
					try:
						handler.handle(request_or_item)
					except Exception as ex:
						logging.info('Exception {} happens when using {}'.format(ex, handler))
						break
				else:
					callback = getattr(spider, request_or_item.callback or 'parse', None)#默认用parse函数
					response = None
					request_response_id = -1
					if request_or_item.use_cache:
						try:
							request_response_map = db.RequestResponseMap.get(request_or_item)
							if request_response_map:
								response = request_response_map.response
								request_response_id = request_response_map.id
						except Exception as ex:
							logging.info('Exception {} happens when try find request map'.format(ex))
							response = None
					if not response:
						while True:
							proxies = self.choose_proxies(request_or_item.url)
							proxies =  {'http': '114.215.24.136:80'}
							try:
								logging.info('try using proxies {}'.format(proxies))
								response = self._network_service.send_request(request_or_item, proxies=proxies, timeout=10)
								if response.status != 200:
									raise Exception('status is not 200, boyd {}'.format(response.body))
								if not spider.is_valid_response(response):
									logging.info('Need validate, escape this proxiey {}'.format(proxies))
								elif not response.url.startswith(request_or_item.url):
									logging.info('Received response.url {} is not the same with request {}, body {}'.\
												 format(response.url, request_or_item.url, response.body))
								else:
									break
							except Exception as ex:
								logging.info('Exception {} happens when sending request with proxies {}'.format(ex, proxies))
								if proxies:
									self.score_proxies(proxies, 0)
						if spider.is_valid_response(response):
							request_response_id = self._store_request_response(request_or_item, response)
					response.set_request_response_id(request_response_id)
					for handler in self._response_handler_list:
						try:
							handler.handle(response)
						except Exception as ex:
							logging.info('Exception {} happens when using {}'.format(ex, handler))
							break
					else:
						if callback:
							try:
								new_request_or_items = callback(response)
							except Exception as ex:
								logging.info('Exception happens when running callback of request {} {}'.format(ex, request_or_item))
								new_request_or_items = []
							self._run(M.arg_to_iter(new_request_or_items), spider)

	def set_network_service(self, network_service):
		self._network_service = network_service

	def add_item_handler(self, item_handler):
		assert isinstance(item_handler, BaseItemHandler), 'item handler must be instance of BaseItemHandler'
		self._item_handler_list.append(item_handler)

	def add_request_handler(self, request_handler):
		assert isinstance(request_handler, BaseRequestHandler), 'request handler must be instance of BaseRequestHandler'
		self._request_handler_list.append(request_handler)

	def add_response_handler(self, response_handler):
		assert isinstance(response_handler, BaseResponseHandler), 'response handler must be instance of BaseResponseHandler'
		self._response_handler_list.append(response_handler)

	def remove_all_handlers(self):
		self._item_handler_list = []
		self._request_handler_list = []
		self._response_handler_list = []

	def _store_request_response(self, request, response):
		request_response_pair = RequestResponseMap(request, response)
		db.merge(request_response_pair)
		db.commit()
		return request_response_pair.id

	def choose_proxies(self, url):
		return ProxyItem.get_proxies(url)
	def score_proxies(self, proxies, score):
		return ProxyItem.score_proxies(proxies, score)


