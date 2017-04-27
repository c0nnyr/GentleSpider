# coding:utf-8
from Request import Request
import re, json, datetime, urllib, urlparse, sys, os, logging, time, math, cPickle

class BaseSpider(object):
	USE_CACHE = False
	VALIDATE_XPATH = None

	start_urls = ()
	metas = ()

	def __init__(self, start_urls=()):
		if start_urls:
			self.start_urls = start_urls
		self.net = None

	def set_network_service(self, net):
		self.net = net
		net.clear()

	def get_start_requests(self):
		if len(self.metas) == len(self.start_urls):
			return [Request(start_url, use_cache=self.USE_CACHE, meta=meta.copy()) for start_url, meta in zip(self.start_urls, self.metas)]
		else:
			return [Request(start_url, use_cache=self.USE_CACHE) for start_url in self.start_urls]

	def parse(self, response):
		pass

	def try_validate(self, response, proxy, timeout):
		return response

	def is_valid_response(self, response):
		return bool(response.xpath(self.VALIDATE_XPATH)) if self.VALIDATE_XPATH else None#至少存在这个

	def _parse_items(self, response, item_xpath, attr_map, item_cls, meta_store_attrs=('start_url',), dct_handler=None):
		sel_items = response.xpath(item_xpath)
		for sel in sel_items:
			dct = {}
			for attr, item in attr_map.iteritems():
				default = item.get('default')
				xpath = item.get('xpath')
				re_filter = item.get('re_filter')
				handler = item.get('handler')

				jump_to_end = False
				if not xpath:
					val = sel.extract()
				else:
					val = ''.join(sel.xpath(xpath).extract()).strip()#对于year_built，有多项
					if not val:
						val = default
						jump_to_end = True
				if not jump_to_end and re_filter:
					try:
						val = re.search(re_filter, val).group('extract')
					except:
						val = default
						jump_to_end = True
				if not jump_to_end and handler:
					try:
						val = handler(val)
					except:
						val = default
						jump_to_end = True
				dct[attr] = val
			if dct_handler:
				dct = dct_handler(response, dct)

			dct.update({'meta_' + k:v for k, v in (response.meta or {}).iteritems() if k in meta_store_attrs})

			#body = response.body
			#dct['_response_body'] = cPickle.dumps(body if isinstance(body, unicode) else body.decode('utf-8'))
			#dct['_request_response_id'] = response.id
			dct['_cur_url'] = response.url
			dct['_crawl_date'] = datetime.datetime.now()

			yield item_cls(**dct)

	def _parse_img(self, response):
		#没有返回一个item处理,而是自己消化了存储了,
		parser = urlparse.urlsplit(response.url)
		img_path = parser.path
		while img_path.startswith('/'):
			img_path = img_path[1:]
		img_path = 'imgs/' + img_path#全部放在imgs目录下
		dirs, _ = os.path.split(img_path)
		if not os.path.exists(dirs):
			os.makedirs(dirs)
		with open(img_path, 'w') as f:
			f.write(response.body)
