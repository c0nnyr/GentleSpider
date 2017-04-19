# coding:utf-8
from BaseLianjiaSpider import BaseLianjiaSpider
import re
from Items import HouseItem
import GlobalMethod as M

class HouseSpider(BaseLianjiaSpider):
	name = 'community'

	BASE_URL = 'http://cd.lianjia.com/ershoufang/%s/{page}co32/'
	
	def __init__(self):
		super(HouseSpider, self).__init__()
		self.start_urls = (
			self.DISTRICT_URL.format(page='') % 'jinjiang',
			self.DISTRICT_URL.format(page='') % 'qingyang',
			self.DISTRICT_URL.format(page='') % 'wuhou',
			self.DISTRICT_URL.format(page='') % 'gaoxing7',
			self.DISTRICT_URL.format(page='') % 'chenghua',
			self.DISTRICT_URL.format(page='') % 'jinniu',
			self.DISTRICT_URL.format(page='') % 'gaoxinxi1',
			self.DISTRICT_URL.format(page='') % 'pidou',
			self.DISTRICT_URL.format(page='') % 'tianfuxinqu',
			self.DISTRICT_URL.format(page='') % 'shuangliu',
			self.DISTRICT_URL.format(page='') % 'wenjiang',
			self.DISTRICT_URL.format(page='') % 'longquanyi',
			self.DISTRICT_URL.format(page='') % 'xindou',
		)

	def parse(self, response):
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
		for item in self._parse_multipage(response, CommunityItem, '/html/body/div[4]/div[1]/ul/li', attr_map, '/html/body/div[4]/div[1]/div[2]/h2/span'):
			yield item

