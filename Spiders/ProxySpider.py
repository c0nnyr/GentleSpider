# coding:utf-8
from BaseSpider import BaseSpider
import re, datetime
from SqlDBHelper import ProxyItem
import GlobalMethod as M
import sys

class BaseProxySpider(BaseSpider):
	digits_pattern = re.compile('^[0-9.]*')
	@classmethod
	def transform_time_to_seconds(cls, t):
		if t is None:
			return sys.maxint
		try:
			digits = float(re.search(cls.digits_pattern, t).group(0))
		except:
			return 0
		if u'毫秒' in t:
			return digits / 1000.0
		elif u'秒' in t:
			return digits
		elif u'分钟' in t:
			return digits * 60
		elif u'小时' in t:
			return digits * 3600
		elif u'天' in t:
			return digits * 3600 * 24
		elif u'年' in t:
			return digits * 3600 * 24 * 365
		else:
			return sys.maxint

class ProxySpider1(BaseProxySpider):
	MAX_PAGE = 5
	start_urls = [ 'http://www.xicidaili.com/nn',] +\
		['http://www.xicidaili.com/nn/{}'.format(ind) for ind in xrange(2, MAX_PAGE)] + \
		['http://www.xicidaili.com/nt/'] + \
		['http://www.xicidaili.com/nt/{}'.format(ind) for ind in xrange(2, MAX_PAGE)]

	def is_valid_response(self, response):
		return bool(response.xpath('//*[@id="ip_list"]'))

	def parse(self, response):
		#xpath = '//*[@id="ip_list"]/tbody/tr[position()>1]'
		xpath = '//*[@id="ip_list"]/tr[position()>1]'#不能有tbody,因为没有thead,tbody是自动生成的
		attr_map = {
			#attr xpath, re_filter
			'country':self.pack('td[1]/img/@alt',),
			'ip':self.pack('td[2]/text()',),
			'port':self.pack('td[3]/text()',),
			'location':self.pack('td[4]/a/text()',),
			'anonymouse_type':self.pack('td[5]/text()',),
			'http_type':self.pack('td[6]/text()', ),
			'speed':self.pack('td[7]/div/@title', ),
			'link_time':self.pack('td[8]/div/@title',),
			'living_time':self.pack('td[9]/text()',),
			'validate_date':self.pack('td[10]/text()', ),
		}

		def post_handler(response, dct):
			#dct['link_time'] = self.transform_time_to_seconds(dct['link_time'])
			#dct['living_time'] = self.transform_time_to_seconds(dct['living_time'])
			#dct['speed'] = self.transform_time_to_seconds(dct['speed'])
			#dct['validate_date'] = datetime.datetime.strptime(dct['validate_date'], '%y-%m-%d %H:%M')
			return dct

		#正式开始解析
		for item in self._parse_items(response, xpath, attr_map, ProxyItem, post_handler):
			yield item

class ProxySpider2(BaseProxySpider):
	MAX_PAGE = 10
	start_urls = ['http://www.kuaidaili.com/free/outha/{}/'.format(ind) for ind in xrange(1, MAX_PAGE)]+\
		['http://www.kuaidaili.com/free/outtr/{}/'.format(ind) for ind in xrange(1, MAX_PAGE)]+ \
		['http://www.kuaidaili.com/free/inha/{}/'.format(ind) for ind in xrange(1, MAX_PAGE)]+ \
		['http://www.kuaidaili.com/free/intr/{}/'.format(ind) for ind in xrange(1, MAX_PAGE)]

	def is_valid_response(self, response):
		return bool(response.xpath('//*[@id="list"]/table'))

	def parse(self, response):
		xpath = '//*[@id="list"]/table/tbody/tr'#这里需要有tbody,因为了thead
		attr_map = {
			#attr xpath, re_filter
			'country':self.pack('', default='undefined'),
			'ip':self.pack('td[1]/text()',),
			'port':self.pack('td[2]/text()',),
			'location':self.pack('td[5]/text()',),
			'anonymouse_type':self.pack('td[3]/text()',),
			'http_type':self.pack('td[4]/text()', ),
			'speed':self.pack('td[6]/text()', ),
			'link_time':self.pack('', default=None),
			'living_time':self.pack('', default=None),
			'validate_date':self.pack('td[7]/text()', ),
		}

		def post_handler(response, dct):
			#dct['link_time'] = self.transform_time_to_seconds(dct['link_time'])
			#dct['living_time'] = self.transform_time_to_seconds(dct['living_time'])
			#dct['speed'] = self.transform_time_to_seconds(dct['speed'])
			#for format in ('%y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S'):
			#	try:
			#		dct['validate_date'] = datetime.datetime.strptime(dct['validate_date'], format)
			#		break
			#	except:
			#		pass
			return dct

		#正式开始解析
		for item in self._parse_items(response, xpath, attr_map, ProxyItem, post_handler):
			yield item
