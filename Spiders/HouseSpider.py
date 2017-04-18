# coding:utf-8
from BaseLianjiaSpider import BaseLianjiaSpider
import re
from Items import HouseItem
import GlobalMethod as M

class HouseSpider(BaseLianjiaSpider):
	name = 'community'

	DISTRICT_URL = 'http://cd.lianjia.com/ershoufang/%s/{page}co32/'
	
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
		#第0阶段就这这里，爬取start_urls的结果
		xpath = '/html/body/div[4]/div[1]/ul/li'
		attr_map = {
			#attr xpath, re_filter
			'url':self.pack('div[1]/div[1]/a/@href',),#这里不能再添加根了，不能/divxx or /li/div
			'id':self.pack('div[1]/div[1]/a/@href', r'(?P<extract>\d+)'),
			'title':self.pack('div[1]/div[1]/a/text()',),
			'desc1':self.pack('div[1]/div[2]/div/text()',),
			'desc2':self.pack('div[1]/div[3]/div/text()',),
			'desc3':self.pack('div[1]/div[4]/div/text()',),

			'total_price':self.pack('div[1]/div[6]/div[1]/span/text()',),
			'price_per_sm':self.pack('div[1]/div[6]/div[2]/span/text()',),
		}

		#正式开始解析
		for item in self._parse_items(response, xpath, attr_map, HouseItem, self.add_page):
			yield item

		district = re.search(r'/ershoufang/(\S*?)/', response.url).group(1)
		for r in self._parse_pages(response, self.DISTRICT_URL % district, '/html/body/div[4]/div[1]/div[2]/h2/span/text()', 30, HouseItem):
			#这里虽然提供了一个总小区个数,但是只提供了100页可以浏览....
			yield r
