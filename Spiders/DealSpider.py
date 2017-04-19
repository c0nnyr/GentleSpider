# coding:utf-8
from BaseLianjiaSpider import BaseLianjiaSpider
import re, logging, math
from Request import Request
from Items import HouseItem
import GlobalMethod as M

class DealSpider(BaseLianjiaSpider):

	BASE_URL = 'http://cd.lianjia.com/chengjiao/{district}/{page}p{price_level}/'
	DISTRICTS = [ 'jinjiang', 'qingyang', 'wuhou', 'gaoxing7', 'chenghua', 'jinniu', \
	              'gaoxinxi1', 'pidou', 'tianfuxinqu', 'shuangliu', 'wenjiang', \
	              'longquanyi', 'xindou',]
	PRICE_LEVELS = [
		4,#80-100
		5,#100-150
		3,#60-80
		2,#40-60
		1,#<40
		6,#150-200
		7,#200-300
		8,#>300
	]

	metas = [{'price_level':price_level, 'district':district} for price_level in PRICE_LEVELS for district in DISTRICTS]
	start_urls = [BASE_URL.format(page='', district=meta['district'], price_level=meta['price_level']) for meta in metas]
	for start_url, meta in zip(start_urls, metas):
		meta['start_url'] = start_url
		meta['page'] = 1

	def is_valid_response(self, response):
		return bool(response.xpath('/html/body/div[4]/div[1]'))

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
		total_pages = response.meta.get('total_pages')

		if total_pages is None:
			total_count_xpath = '/html/body/div[4]/div[1]/div[2]/div[1]/span'
			total_count = int(response.xpath(total_count_xpath).extract_first())
			total_pages = min(int(math.ceil(float(total_count) / self.MAX_COUNT_PER_PAGE)), self.MAX_PAGE)#最多允许爬去100页

		if item_count == self.MAX_COUNT_PER_PAGE and cur_page < total_pages:#说明不是最后一页了
			next_page = cur_page + 1
			url = self.BASE_URL.format(page='pg%d' % next_page, price_level=price_level)
			yield Request(url, meta={'price_level':price_level, 'page':next_page, 'start_url':start_url})
		else:
			logging.info('finish start_url {}'.format(start_url))
		pass
