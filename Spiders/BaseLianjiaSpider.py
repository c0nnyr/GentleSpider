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
		#正式开始解析
		item_count = 0
		for item in self._parse_items(response, item_xpath, item_attr_map, item_cls, self.add_page):
			item_count += 1
			yield item

		cur_page = response.meta['page']
		price_level = response.meta['price_level']
		start_url = response.meta['start_url']
		total_pages = response.meta.get('total_pages')

		if total_pages is None:
			total_count = int(response.xpath(total_count_xpath).extract_first())
			total_pages = min(int(math.ceil(float(total_count) / self.MAX_COUNT_PER_PAGE)), self.MAX_PAGE)#最多允许爬去100页

		if item_count == self.MAX_COUNT_PER_PAGE and cur_page < total_pages:#说明不是最后一页了
			next_page = cur_page + 1
			url = self.BASE_URL.format(page='pg%d' % next_page, price_level=price_level)
			yield Request(url, meta={'price_level':price_level, 'page':next_page, 'start_url':start_url})
		else:
			logging.info('finish start_url {}'.format(start_url))

	@staticmethod
	def add_page(response, dct):
		dct['page'] = response.meta.get('page', 1)
		return dct

	#def is_valid_response(self, response):
		#return 'captcha.lianjia.com/' not in response.url#这个不一定靠谱了

	#def try_validate(self, response, func):
	#	if not self.is_valid_response(response):
	#		print 'validating...'
	#		#csrf_xpath = '/html/body/div/div[2]/div[1]/ul/form/input[3]/@value'#does not work, cannot find form
	#		#csrf = response.xpath(csrf_xpath).extract_first()
	#		#似乎form不太好用xpath处理
	#		try:
	#			csrf = re.search(r'name="_csrf" value="(?P<extract>\S*?)"', response.body).group('extract')
	#			url = urllib.unquote(re.search(r'redirect=(?P<extract>.*)', response.url).group('extract'))
	#			print 'original_url', url
	#			meta = {'_validate_csrf':csrf, '_validate_func':func, '_validate_url':url}
	#			meta.update(response.meta)
	#			yield Request(self.VALIDATE_IMG_URL, callback='_parse_validate_imgs', meta=meta, dont_filter=True)#不参与去重
	#		except:
	#			print 'cannot find csrf in ', response.body

	#def _parse_validate_imgs(self, response):
	#	dct = json.loads(response.body)
	#	csrf = response.meta.get('_validate_csrf')
	#	formdata = {'_csrf':csrf, 'uuid':dct['uuid'], 'bitvalue':'2'}
	#	meta = {'_validate_csrf':csrf, '_validate_func':response.meta.get('_validate_func'), '_validate_url':response.meta.get('_validate_url')}
	#	meta.update(response.meta)
	#	yield Request(self.VALIDATE_IMG_URL, method='post', callback='_try_validate_once', data=formdata, meta=meta, dont_filter=True)

	#def _try_validate_once(self, response):
	#	print response.body, response.url
	#	if '"error":true' in response.body:
	#		csrf = response.meta.get('_validate_csrf')
	#		meta = {'_validate_csrf':csrf, '_validate_func':response.meta.get('_validate_func'), '_validate_url':response.meta.get('_validate_url')}
	#		meta.update(response.meta)
	#		yield Request(self.VALIDATE_IMG_URL, callback='_parse_validate_imgs', meta=meta, dont_filter=True)
	#	else:
	#		print 'finish validating'
	#		func = response.meta.get('_validate_func')
	#		yield Request(response.meta.get('_validate_url'), callback=func, meta=response.meta)
