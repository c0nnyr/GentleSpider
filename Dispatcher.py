# coding:utf-8
from BaseObject import BaseObject
from BaseHandler import BaseItemHandler, BaseRequestHandler, BaseResponseHandler
from BaseSpider import BaseSpider
from Request import Request
import GlobalMethod as M
import itertools, logging
from SqlDBHelper import ProxyItem, RequestResponseMap

class Dispatcher(BaseObject):
	REQUEST_COUNT_THRESHOLD = 10
	PROXY_TIMEOUT = 3

	DEPTH_MODE = 0
	WIDTH_MODE = 1

	def __init__(self):
		super(Dispatcher, self).__init__()
		self._network_service = None
		self._item_handler_list = []
		self._request_handler_list = []
		self._response_handler_list = []
		self._proxies = None
		self._cur_proxy_request_count = 0
		self._score_proxy = True
		self._use_proxy = True
		self._mode = self.DEPTH_MODE

	def set_config(self, config):
		self._mode = config.get('mode', self._mode)
		self._use_proxy = config.get('use_proxy', self._use_proxy)
		self._score_proxy = config.get('score_proxy', self._score_proxy)

	def run(self, *spiders):
		for handler in itertools.chain(self._item_handler_list, self._response_handler_list, self._request_handler_list):
			handler.open_spider()
		for spider in spiders:
			assert isinstance(spider, BaseSpider), 'spider must be instance of BaseSpider'
			spider.set_network_service(self._network_service)
			request_or_items = spider.get_start_requests()
			self._run(M.arg_to_iter(request_or_items), spider)
		for handler in itertools.chain(self._item_handler_list, self._response_handler_list, self._request_handler_list):
			handler.close_spider()

	def _run(self, request_or_items, spider):
		request_or_items_list = list(request_or_items)
		while True:
			if not request_or_items_list:
				break
			request_or_item = request_or_items_list.pop(0)
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
							request_response_map = RequestResponseMap.get(request_or_item)
							if request_response_map:
								response = request_response_map.response
								request_response_id = request_response_map.id
						except Exception as ex:
							logging.info('Exception {} happens when try find request map'.format(ex))
							response = None
					if not response:
						while True:
							if self._use_proxy:
								if not self._proxies or self._cur_proxy_request_count > self.REQUEST_COUNT_THRESHOLD:
									self._proxies = self.choose_proxies(request_or_item.url)
									logging.info('try using proxies {}'.format(self._proxies))
									if self._proxies:
										self._cur_proxy_request_count = 0
							try:
								response = self._network_service.send_request(request_or_item, proxies=self._proxies, timeout=self.PROXY_TIMEOUT)
								response = spider.try_validate(response)
								if not response:
									raise Exception('response is None after try validate')
								elif response.status != 200:
									raise Exception('status is not 200, body {}'.format(response.body))
								elif not spider.is_valid_response(response):
									raise Exception('not valid response {}, escape this proxiey {}'.format(response.body, self._proxies))
								else:
									self._cur_proxy_request_count += 1
									break
							except Exception as ex:
								logging.info('Exception {} happens when sending request with proxies {}'.format(ex, self._proxies))
								if self._proxies:
									if self._score_proxy and self._cur_proxy_request_count == 0:
										self.score_proxies(self._proxies, 0)
									self._proxies = None
								else:
									raise ex
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
							new_request_or_items = list(M.arg_to_iter(new_request_or_items))
							new_items = [item for item in new_request_or_items if M.is_item(item)]
							new_requests = [request for request in new_request_or_items if not M.is_item(request)]
							if self._mode == self.DEPTH_MODE:
								request_or_items_list[0:0] = new_request_or_items
							elif self._mode == self.WIDTH_MODE:
								request_or_items_list.extend(new_requests)
								request_or_items_list[0:0] = new_items

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
		return RequestResponseMap.store(request, response)

	def choose_proxies(self, url):
		return ProxyItem.get_proxies(url)
	def score_proxies(self, proxies, score):
		return ProxyItem.score_proxies(proxies, score)


