# coding:utf-8
from BaseObject import BaseObject
from BaseItemHandler import BaseItemHandler
from BaseSpider import BaseSpider
from Request import Request
import GlobalMethod as M

class Dispatcher(BaseObject):

	def __init__(self):
		super(Dispatcher, self).__init__()
		self._network_service = None
		self._item_handler_list = []

	def run(self, spider):
		assert isinstance(spider, BaseSpider), 'spider must be instance of BaseSpider'
		request_or_items = spider.get_start_requests()
		self._run(M.arg_to_iter(request_or_items))

	def _run(self, request_or_items):
		for request_or_item in request_or_items:
			if M.is_item(request_or_item):
				for handler in self._item_handler_list:
					try:
						handler.handle(request_or_item)
					except Exception as ex:
						print 'Exception happens when using', ex, handler
			elif isinstance(request_or_item, Request):
				callback = request_or_item.callback
				response = self._network_service.send_request(request_or_item)
				if callback:
					try:
						new_request_or_items = callback(response)
					except Exception as ex:
						print 'Exception happens when running callback of request', ex, request_or_item
						new_request_or_items = []
					self._run(M.arg_to_iter(new_request_or_items))

	def set_network_service(self, network_service):
		self._network_service = network_service

	def set_item_handler(self, item_handler):
		assert isinstance(item_handler, BaseItemHandler), 'item handler must be instance of BaseItemHandler'
		self._item_handler_list.append(item_handler)

