# coding:utf-8
from Request import Request
import re, json

class BaseSpider(object):
	USE_CACHE = False
	start_urls = ()
	metas = ()

	def __init__(self, start_urls=()):
		if start_urls:
			self.start_urls = start_urls
		self.net = None

	def set_network_service(self, net):
		self.net = net

	def get_start_requests(self):
		if len(self.metas) == len(self.start_urls):
			return [Request(start_url, use_cache=self.USE_CACHE, meta=meta) for start_url, meta in zip(self.start_urls, self.metas)]
		else:
			return [Request(start_url, use_cache=self.USE_CACHE) for start_url in self.start_urls]

	def parse(self, response):
		pass

	def try_validate(self, response):
		return response

	def is_valid_response(self, response):
		return True

	@staticmethod
	def pack(xpath, re_filter=None, default=0):
		#设置好xpath,re提取,默认值
		return xpath, re_filter, default#这个辅助解包用好

	def _parse_items(self, response, item_xpath, attr_map, item_cls, dct_handler=None):
		sel_items = response.xpath(item_xpath)
		for sel in sel_items:
			dct = {}
			for attr, item in attr_map.iteritems():
				xpath, re_filter, default = item
				if not xpath:
					content = default
				else:
					content = ''.join(sel.xpath(xpath).extract())#对于year_built，有多项
					if re_filter:
						try:
							content = re.search(re_filter, content).group('extract')
						except:
							content = default
				dct[attr] = content
			if dct_handler:
				dct = dct_handler(response, dct)
			dct['start_url'] = response.meta.get('start_url', response.url)
			dct['original_data'] = json.dumps(dct)
			dct['meta'] = json.dumps(response.meta)
			yield item_cls(request_response_id=response.id, **dct)
