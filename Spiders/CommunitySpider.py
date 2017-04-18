# coding:utf-8
from BaseLianjiaSpider import BaseLianjiaSpider
import re, logging
from Items import CommunityItem
import GlobalMethod as M
from Request import Request

class CommunitySpider(BaseLianjiaSpider):
	name = 'community'

	COMMUNITY_URL = 'http://cd.lianjia.com/xiaoqu/{page}p{price_level}/'
	metas = [
		{'price_level':4},#1~1.5
		{'price_level':5},#1.5~2
		{'price_level':3},#0.8~1
		{'price_level':2},#0.5~0.8
		{'price_level':1},#<0.5
		{'price_level':6},#>2
	]
	start_urls = [COMMUNITY_URL.format(page='', price_level=meta['price_level']) for meta in metas]
	for start_url, meta in zip(start_urls, metas):
		meta['start_url'] = start_url
		meta['page'] = 1

	def is_valid_response(self, response):
		return bool(response.xpath('/html/body/div[4]/div[1]'))#至少存在这个

	def parse(self, response):
		#第0阶段就这这里，爬取start_urls的结果
		xpath = '/html/body/div[4]/div[1]/ul/li'
		attr_map = {
			#attr xpath, re_filter
			'url':self.pack('div[2]/div[2]/a/@href',),#这里不能再添加根了，不能/divxx or /li/div
			'id':self.pack('div[2]/div[2]/a/@href', r'(?P<extract>\d+)'),
			'title':self.pack('div[1]/div[1]/a/text()',),
			'count_on_sale':self.pack('div[2]/div[2]/a/span/text()',),
			'price_per_sm':self.pack('div[2]/div[1]/div[1]/span/text()',),
			'count_on_rent':self.pack('div[1]/div[2]/a[2]/text()', r'(?P<extract>\d+)'),
			'count_sold_90days':self.pack('div[1]/div[2]/a[1]/text()', r'90\S+(?P<extract>\d+)'),
			'district':self.pack('div[1]/div[3]/a[1]/text()',),
			'bizcircle':self.pack('div[1]/div[3]/a[2]/text()',),
			'year_built':self.pack('div[1]/div[3]/text()',  r'(?P<extract>\d+)', '0'),
		}

		#正式开始解析
		item_count = 0
		for item in self._parse_items(response, xpath, attr_map, CommunityItem, self.add_page):
			item_count += 1
			yield item

		cur_page = response.meta['page']
		price_level = response.meta['price_level']
		start_url = response.meta['start_url']
		if item_count == 30 and cur_page < 100:#说明不是最后一页了
			url = self.COMMUNITY_URL.format(page='pg%d' % cur_page + 1, price_level=price_level)
			yield Request(url, meta={'price_level':price_level, 'page':cur_page + 1, 'start_url':start_url})
		else:
			logging.info('finish start_url {}'.format(start_url))
