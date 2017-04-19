# coding:utf-8
from BaseSpider import BaseSpider
import math, re, json, urllib
from Request import Request
import logging

class BaseLianjiaSpider(BaseSpider):

	MAX_COUNT_PER_PAGE = 30
	MAX_PAGE = 100

	VALIDATE_XPATH = None
	BASE_URL = None

	def is_valid_response(self, response):
		return bool(response.xpath(self.VALIDATE_XPATH))#至少存在这个

	def _parse_multipage(self, response, item_cls, item_xpath, item_attr_map, total_count_xpath):
		item_count = 0
		for item in self._parse_items(response, item_xpath, item_attr_map, item_cls, self.add_page):
			item_count += 1
			yield item

		start_url = response.meta['start_url']

		cur_page = response.meta.get('page', 1)
		total_pages = response.meta.get('total_pages')

		if total_pages is None:
			total_count = int(response.xpath(total_count_xpath).extract_first())
			total_pages = min(int(math.ceil(float(total_count) / self.MAX_COUNT_PER_PAGE)), self.MAX_PAGE)#最多允许爬去100页

		if item_count == self.MAX_COUNT_PER_PAGE and cur_page < total_pages:#说明不是最后一页了
			url = self._get_next_page_url(response)
			if url:
				meta = dict(**response.meta)
				meta['page'] = cur_page + 1
				yield Request(url, meta=meta)
		else:
			logging.info('finish start_url {}'.format(start_url))

	def _get_next_page_url(self, response):
		dct = dict(**response.meta)
		dct['page'] = 'pg%d' % (dct.get('page', 1) + 1)#用于构建url
		return self.BASE_URL.format(**dct)

	@staticmethod
	def add_page(response, dct):
		dct['page'] = response.meta.get('page', 1)
		return dct
