# coding:utf-8
from Request import Request
import re, json, datetime, urllib, urlparse, sys, os, logging, time, math, cPickle
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy


class BaseSpider(object):
	VALIDATE_XPATH = None

	start_urls = ()
	metas = ()

	START_FROM_LIKE_URL = None#从这个start url 继续开始

	def __init__(self):
		self.net = None
		self.config = {}
		self.session = None

	def destroy(self):
		if self.session:
			self.session.close()
			self.session = None

	def get_session(self):
		return self.session

	def set_config(self, config):
		self.config.update(config)

	def set_network_service(self, net):
		self.net = net
		net.clear()

	def get_start_requests(self):
		if len(self.metas) == len(self.start_urls):
			rets = [Request(start_url, meta=meta.copy()) for start_url, meta in zip(self.start_urls, self.metas)]
		else:
			rets = [Request(start_url, ) for start_url in self.start_urls]
		if self.START_FROM_LIKE_URL:
			for ind, r in enumerate(rets):
				if self.START_FROM_LIKE_URL in r.url:
					return rets[ind:]
		return rets

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
					if xpath is None:
						val = default
					else:
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
