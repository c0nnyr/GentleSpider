# coding:utf-8
from BaseObject import BaseObject
from BaseItem import BaseItem
class Dispatcher(BaseObject):

	def __init__(self):
		super(Dispatcher, self).__init__()
		self._network_service = None
		self._item_handler = None

	@staticmethod
	def arg_to_iter(arg):
		if arg is None:
			return []
		elif not isinstance(arg, BaseItem) and hasattr(arg, '__iter__'):
			return arg
		else:
			return [arg]

	def run(self, spider):
		request_or_items = spider.get_start_requests()
		self._run(self.arg_to_iter(request_or_items))

	def _run(self, request_or_items):
		for request_or_item in request_or_items:
			if isinstance(request_or_item, BaseItem):
				self._item_handler(request_or_item)
			else:
				callback = request_or_item.callback
				response = self._network_service.send_request(request_or_item)
				new_request_or_items = callback(response)
				self._run(new_request_or_items)

	def set_network_service(self, network_service):
		self._network_service = network_service

	def set_item_handler(self, item_handler):
		self._item_handler = item_handler

