# coding:utf-8
from BaseSpider import BaseSpider
import math, re, json, urllib
from Request import Request
import logging, time

class BaseLianjiaSpider(BaseSpider):

	MAX_COUNT_PER_PAGE = 30
	MAX_PAGE = 100

	VALIDATE_XPATH = None
	BASE_URL = None

	CHECK_HAS_CRAWLED_PAGE = False

	VALIDATE_IMG_URL = 'http://captcha.lianjia.com/human'

	TRY_VALIDATE_THRESHOLD = 200
	VALIDATE_TIME_RESET_DURATION = 10 * 60#十分钟重置一下

	def __init__(self):
		super(BaseLianjiaSpider, self).__init__()
		self._try_validate_count = 0
		self._validate_time = 0

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

		if item_count == self.MAX_COUNT_PER_PAGE:
			next_page = cur_page + 1
			while next_page <= total_pages:
				url = self._get_next_page_url(response, next_page)
				if self.CHECK_HAS_CRAWLED_PAGE and item_cls.check_page_crawled(next_page, start_url):
					logging.info('has crawed page {} ind, url {}'.format(next_page, url))
					next_page += 1
					continue
				if url:
					meta = dict(**response.meta)
					meta['page'] = next_page
					logging.info('total pages {}, ready to request {}'.format(total_pages, next_page))
					yield Request(url, meta=meta)
				break
		else:
			logging.info('finish start_url {}'.format(start_url))

	def _get_next_page_url(self, response, next_page):
		dct = dict(**response.meta)
		dct['page'] = 'pg%d' % next_page#用于构建url
		return self.BASE_URL.format(**dct)

	@staticmethod
	def add_page(response, dct):
		dct['page'] = response.meta.get('page', 1)
		return dct

	def try_validate(self, response):
		if self.is_valid_response(response):
			return response
		original_url = urllib.unquote(re.search(r'redirect=(?P<extract>.*)', response.url).group('extract'))
		original_meta = response.meta
		logging.info('validating...')
		#csrf_xpath = '/html/body/div/div[2]/div[1]/ul/form/input[3]/@value'#does not work, cannot find form
		#csrf = response.xpath(csrf_xpath).extract_first()
		#似乎form不太好用xpath处理
		csrf = re.search(r'name="_csrf" value="(?P<extract>\S*?)"', response.body).group('extract')
		while True:
			if time.time() - self._validate_time > self.VALIDATE_TIME_RESET_DURATION:
				self._try_validate_count = 0
			self._try_validate_count += 1
			if self._try_validate_count > self.TRY_VALIDATE_THRESHOLD:
				return None

			response = self.net.send_request(Request(self.VALIDATE_IMG_URL))
			dct = json.loads(response.body)
			formdata = {'_csrf':csrf, 'uuid':dct['uuid'], 'bitvalue':'2'}
			time.sleep(1)
			response = self.net.send_request(Request(self.VALIDATE_IMG_URL, method='post', data=formdata))

			if '"error":true' not in response.body:
				logging.info('finish validating')
				time.sleep(1)
				return self.net.send_request(Request(original_url, meta=original_meta))
