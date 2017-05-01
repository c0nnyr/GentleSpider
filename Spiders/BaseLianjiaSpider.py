# coding:utf-8
from BaseSpider import BaseSpider
import math, re, json, urllib
from Request import Request
import logging, time, collections
import GlobalMethod as M
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
import random, datetime, collections

_Model = declarative_base(name='validation')
class ValidationItem(_Model):
	__tablename__ = 'validation'
	id = Column(Integer(), autoincrement=True, primary_key=True)
	_crawl_date = Column(DateTime())
	bitvalue = Column(Integer())

	all_bitvalues = None
	THRESHOLD_COUNT = 1000

	@classmethod
	def initialize(cls, session):
		if cls.all_bitvalues is None:
			cls.all_bitvalues = collections.defaultdict(lambda :0)
			for bitvalue, in session.query(cls.bitvalue):
				cls.all_bitvalues[bitvalue] += 1
	@classmethod
	def get_possible_bitvalue(cls, session):
		if sum(cls.all_bitvalues.itervalues()) < cls.THRESHOLD_COUNT:#超过100
			return random.choice(range(1, 16))
		else:
			return sorted(cls.all_bitvalues.iterkeys(), lambda k:cls.all_bitvalues[k], reverse=True)[0]

	@classmethod
	def save(cls, session, bitvalue):
		if sum(cls.all_bitvalues.itervalues()) >= cls.THRESHOLD_COUNT:#超过100
			return
		cls.all_bitvalues[bitvalue] += 1

		item = cls()
		item.bitvalue = bitvalue
		item._crawl_date = datetime.datetime.now()
		session.add(item)
		session.commit()

validation_session = M.create_engine('validation', _Model)

class BaseLianjiaSpider(BaseSpider):

	MAX_COUNT_PER_PAGE = 30
	MAX_PAGE = 100

	BASE_URL = None

	VALIDATE_IMG_URL = 'http://captcha.lianjia.com/human'

	TRY_VALIDATE_THRESHOLD = 30

	def _parse_multipage(self, response, item_cls, item_xpath, item_attr_map, total_count_xpath, meta_store_attrs):
		item_count = 0
		existed_count = 0
		for item in self._parse_items(response, item_xpath, item_attr_map, item_cls, meta_store_attrs):
			item_count += 1
			if self.config.get('need_check_existence') and item.check_existence(self.session):
				existed_count += 1
			else:
				yield item

		if existed_count > self.MAX_COUNT_PER_PAGE / 3:
			logging.info('*******finished this meta {} with existed_count {}'.format(response.meta, existed_count))
			return
		elif existed_count > 0:
			logging.info('existing count {}'.format(existed_count))

		start_url = response.meta['start_url']
		cur_page = response.meta.get('page', 1)
		total_pages = response.meta.get('total_pages')

		if total_pages is None:
			total_count = int(response.xpath(total_count_xpath).extract_first())
			total_pages = min(int(math.ceil(float(total_count) / self.MAX_COUNT_PER_PAGE)), self.MAX_PAGE)#最多允许爬去100页

		if item_count == self.MAX_COUNT_PER_PAGE:
			next_page = cur_page + 1
			if next_page <= total_pages:
				url = self._get_page_url(response.meta, next_page)
				#if self.CHECK_HAS_CRAWLED_PAGE and item_cls.check_page_crawled(page=next_page, start_url=start_url, url=url):
					#logging.info('has crawed page {} ind, url {}'.format(next_page, url))
					#next_page += 1
					#continue
				meta = response.meta.copy()
				meta['page'] = next_page
				meta['total_pages'] = total_pages
				logging.info('total pages {}, ready to request {}'.format(total_pages, next_page))
				yield Request(url, meta=meta)
		else:
			logging.info('finish start_url {}'.format(start_url))

	def _get_page_url(self, meta, page):
		dct = meta.copy()
		dct['page'] = 'pg%d' % page#用于构建url
		return self.BASE_URL.format(**dct)

	def try_validate(self, response, proxy, timeout):
		if self.is_valid_response(response):
			return response
		original_response = response
		try_validate_count = 0
		ValidationItem.initialize(validation_session)
		try:
			original_url = urllib.unquote(re.search(r'redirect=(?P<extract>.*)', response.url).group('extract'))
			original_meta = response.meta
			logging.info('validating...')
			#csrf_xpath = '/html/body/div/div[2]/div[1]/ul/form/input[3]/@value'#does not work, cannot find form
			#csrf = response.xpath(csrf_xpath).extract_first()
			#似乎form不太好用xpath处理
			csrf = re.search(r'name="_csrf" value="(?P<extract>\S*?)"', response.body).group('extract')
			while True:
				try_validate_count += 1
				if try_validate_count > self.TRY_VALIDATE_THRESHOLD:
					return original_response
				logging.info('{} / {} of validate'.format(try_validate_count, self.TRY_VALIDATE_THRESHOLD))

				response = self.net.send_request(Request(self.VALIDATE_IMG_URL), proxies=proxy, timeout=timeout)
				try:
					dct = json.loads(response.body)#可能返回的还是一个验证的网站
				except:
					logging.info('may return non json content, but validate page, try again')
					csrf = re.search(r'name="_csrf" value="(?P<extract>\S*?)"', response.body).group('extract')
					response = self.net.send_request(Request(self.VALIDATE_IMG_URL), proxies=proxy, timeout=timeout)
					dct = json.loads(response.body)
				bitvalue = ValidationItem.get_possible_bitvalue(validation_session)
				formdata = {'_csrf':csrf, 'uuid':dct['uuid'], 'bitvalue':str(bitvalue)}
				time.sleep(1)
				response = self.net.send_request(Request(self.VALIDATE_IMG_URL, method='post', data=formdata), \
												 proxies=proxy, timeout=timeout)

				if '"error":true' not in response.body:
					ValidationItem.save(validation_session, bitvalue)
					logging.info('finish validating')
					time.sleep(1)
					return self.net.send_request(Request(original_url, meta=original_meta), proxies=proxy, timeout=timeout)
		except Exception as ex:
			logging.info('try validate exception {} with response body {}'.format(ex, response.body))
			return original_response
