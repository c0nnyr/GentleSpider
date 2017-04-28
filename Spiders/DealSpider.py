# coding:utf-8
from BaseLianjiaSpider import BaseLianjiaSpider
import GlobalMethod as M
from Items import DealItem

class DealSpider(BaseLianjiaSpider):

	VALIDATE_XPATH = '/html/body/div[4]/div[contains(@class,"leftContent")]'

	BASE_URL_CD = 'http://cd.lianjia.com/chengjiao/{district}/{page}a{area}p{price_level}/'
	DISTRICTS_CD = [ 'jinjiang', 'qingyang', 'wuhou', 'gaoxing7', 'chenghua', 'jinniu', \
	              'gaoxinxi1', 'pidou', 'tianfuxinqu', 'shuangliu', 'wenjiang', \
	              'longquanyi', 'xindou',]
	PRICE_LEVELS_CD = [
		4,#80-100
		5,#100-150
		3,#60-80
		2,#40-60
		1,#<40
		6,#150-200
		7,#200-300
		8,#>300
	]

	BASE_URL_HZ = 'http://hz.lianjia.com/chengjiao/{district}/{page}a{area}p{price_level}/'
	DISTRICTS_HZ = ['xihu', 'xiacheng', 'jianggan', 'gongshu', 'shangcheng', 'binjiang', \
					'yuhang', 'xiaoshan', 'xiasha']
	PRICE_LEVELS_HZ = [
		4,#200-300
		5,#300-500
		3,#150-200
		2,#100-150
		1,#<100
		6,#>500
	]

	AREAS = [
		1,#<50
		2,#50~70
		3,#70~90
		4,#90~110
		5,#110~130
		6,#130~150
		7,#150~200
		8,#>200
	]
	#DIRECTIONS = [#链家自己的分类问题很多,还是沿着以前的分类
		#1,
		#2,
		#3,
		#4,
		#5,
	#]

	def __init__(self, city='cd'):
		super(DealSpider, self).__init__()
		if city == 'cd':
			self.metas = [{'price_level':price_level, 'district':district, 'area':area, }
					 for price_level in self.PRICE_LEVELS_CD
					 for district in self.DISTRICTS_CD
					 for area in self.AREAS ]
			self.BASE_URL = self.BASE_URL_CD
		elif city == 'hz':
			self.metas = [{'price_level':price_level, 'district':district, 'area':area, }
						  for price_level in self.PRICE_LEVELS_HZ
						  for district in self.DISTRICTS_HZ
						  for area in self.AREAS ]
			self.BASE_URL = self.BASE_URL_HZ
		else:
			raise Exception('not supported city')

		self.start_urls = M.fill_meta_extract_start_urls(self.BASE_URL, self.metas)

	def parse(self, response):
		attr_map = {
			#attr xpath, re_filter
			'url':dict(xpath='div/div[1]/a/@href',),#这里不能再添加根了，不能/divxx or /li/div
			'deal_id':dict(xpath='div/div[1]/a/@href', re_filter=r'chengjiao/(?P<extract>\S+)\.'),
			'deal_date':dict(xpath='div/div/div[contains(@class, "dealDate")]/text()',),
			'title':dict(xpath='div/div[1]/a/text()',),
			'house_info':dict(xpath='div/div/div[contains(@class, "houseInfo")]/text()',),
			'total_price':dict(xpath='div/div/div[contains(@class, "totalPrice")]/span/text()',),
			'position_info':dict(xpath='div/div/div[contains(@class, "positionInfo")]/text()',),
			'deal_platform':dict(xpath='div/div/div[contains(@class, "source")]/text()',),
			'unit_price':dict(xpath='div/div/div[contains(@class, "unitPrice")]/span/text()',),
			'deal_house_text':dict(xpath='div/div/span[contains(@class, "dealHouseTxt")]/span/text()',),
			'deal_cycle_txt':dict(xpath='div/div/span[contains(@class, "dealCycleTxt")]/span/text()',),
		}
		for item in self._parse_multipage(response, DealItem, '/html/body/div[4]/div[1]/ul/li', attr_map,
										  '/html/body/div[4]/div[1]/div[2]/div[1]/span/text()',
										  ('district', 'price_level', 'area', 'start_url')):
			yield item
