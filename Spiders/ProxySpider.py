# coding:utf-8
from BaseSpider import BaseSpider
import re, datetime
from SqlDBHelper import ProxyItem
import GlobalMethod as M
import sys, json

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
	MAX_PAGE = 2
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
			'country':dict(xpath='td[1]/img/@alt',),
			'ip':dict(xpath='td[2]/text()',),
			'port':dict(xpath='td[3]/text()',),
			'location':dict(xpath='td[4]/a/text()',),
			'anonymouse_type':dict(xpath='td[5]/text()',),
			'http_type':dict(xpath='td[6]/text()', ),
			'speed':dict(xpath='td[7]/div/@title', ),
			'link_time':dict(xpath='td[8]/div/@title',),
			'living_time':dict(xpath='td[9]/text()',),
			'validate_date':dict(xpath='td[10]/text()', ),
		}

		#正式开始解析
		for item in self._parse_items(response, xpath, attr_map, ProxyItem, ):
			yield item

class ProxySpider2(BaseProxySpider):
	MAX_PAGE = 5
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
			'country':dict(default=None),
			'ip':dict(xpath='td[1]/text()',),
			'port':dict(xpath='td[2]/text()',),
			'location':dict(xpath='td[5]/text()',),
			'anonymouse_type':dict(xpath='td[3]/text()',),
			'http_type':dict(xpath='td[4]/text()', ),
			'speed':dict(xpath='td[6]/text()', ),
			'link_time':dict(default=None),
			'living_time':dict(default=None),
			'validate_date':dict(xpath='td[7]/text()', ),
		}

		#正式开始解析
		for item in self._parse_items(response, xpath, attr_map, ProxyItem, ):
			yield item

class ProxySpider3(BaseProxySpider):
	MAX_PAGE = 5
	start_urls = ['http://www.proxy360.cn/Region/Brazil',
				  'http://www.proxy360.cn/Region/China',
				  'http://www.proxy360.cn/Region/America',
				  'http://www.proxy360.cn/Region/Taiwan',
				  'http://www.proxy360.cn/Region/Japan',
				  'http://www.proxy360.cn/Region/Thailand',
				  'http://www.proxy360.cn/Region/Vietnam',
				  'http://www.proxy360.cn/Region/bahrein',
				  ]

	def is_valid_response(self, response):
		return bool(response.xpath('//*[@id="ctl00_ContentPlaceHolder1_upProjectList"]/div[1]'))

	def parse(self, response):
		xpath = '//div[contains(@class, "proxylistitem")]/div[1]'#这里需要有tbody,因为了thead
		attr_map = {
			#attr xpath, re_filter
			'country':dict(xpath='span[4]/text()',),
			'ip':dict(xpath='span[1]/text()',),
			'port':dict(xpath='span[2]/text()',),
			'location':dict(default=None),
			'anonymouse_type':dict(xpath='span[3]/text()',),
			'http_type':dict(default='HTTP'),
			'speed':dict(defalt=None),
			'link_time':dict(defalt=None),
			'living_time':dict(defalt=None),
			'validate_date':dict(xpath='span[5]/text()', ),
		}

		#正式开始解析
		for item in self._parse_items(response, xpath, attr_map, ProxyItem, ):
			yield item

class ProxySpider4(BaseProxySpider):
	MAX_PAGE = 10
	start_urls = ['http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10',
				  ]

	def is_valid_response(self, response):
		return True

	def parse(self, response):
		json_txt = eval(response.body).decode('utf-8')
		for row in json.loads(json_txt)['rows']:
			attr_map = {
				#attr xpath, re_filter
				'country':'undefined',
				'ip':row['ip'],
				'port':row['port'],
				'location':row['position'],
				'anonymouse_type':row['anony'],
				'http_type':'HTTP',
				'speed':row['responsetime'],
				'link_time':None,
				'living_time':None,
				'validate_date':row['createTime'],

				'start_url':response.meta.get('start_url', response.url),
				'original_data':json_txt,#必须是unicode的,里面有中文,否则数据库不知道怎么办
				'meta':json.dumps(response.meta),
			}
			yield ProxyItem(**attr_map)


cls_list = [ProxySpider1, ProxySpider2, ProxySpider3, ProxySpider4]
cls_list = [ProxySpider2, ProxySpider3, ProxySpider4]
