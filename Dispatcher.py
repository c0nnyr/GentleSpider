# coding:utf-8
from BaseObject import BaseObject
from BaseHandler import BaseItemHandler, BaseRequestHandler, BaseResponseHandler
from BaseSpider import BaseSpider
from Request import Request
import GlobalMethod as M
import itertools, logging
import SqlDBHelper as db


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
						logging.info('Exception happens when using {}, {}'.format(ex, handler))
			elif isinstance(request_or_item, Request):
				for handler in self._request_handler_list:
					try:
						handler.handle(request_or_item)
					except Exception as ex:
						logging.info('Exception happens when using {} {}'.format(ex, handler))
						break
				else:
					callback = request_or_item.callback or spider.parse
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
						response = self._network_service.send_request(request_or_item)
						if spider.is_valid_response(response):
							request_response_id = self._store_request_response(request_or_item, response)
					response.set_request_response_id(request_response_id)
					for handler in self._response_handler_list:
						try:
							handler.handle(response)
						except Exception as ex:
							logging.info('Exception happens when using {} {}'.format(ex, handler))
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

	def _store_request_response(self, request, response):
		request_response_pair = db.RequestResponseMap(request, response)
		db.session.merge(request_response_pair)
		db.session.commit()
		return request_response_pair.id

