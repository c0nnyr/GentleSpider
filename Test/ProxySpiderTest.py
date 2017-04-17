# coding:utf-8
from BaseSpider import BaseSpider
from Items import ProxyItem
import re, math, json, datetime
from Request import Request
import GlobalMethod as M

class ProxySpiderTest(BaseSpider):
	start_urls = (
		'http://www.xicidaili.com/nn',#国内高匿代理
	)

	def parse(self, response):
		#xpath = '//*[@id="ip_list"]/tbody/tr[position()>1]'
		xpath = '//*[@id="ip_list"]/tr[position()>1]'#不能有tbody,很奇怪
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
		digits_pattern = re.compile('^[0-9.]*')
		def transform_time_to_seconds(t):
			digits = float(re.search(digits_pattern, t).group(0))
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
				return 1000000000#超过1年

		def post_handler(response, dct):
			dct['link_time'] = transform_time_to_seconds(dct['link_time'])
			dct['living_time'] = transform_time_to_seconds(dct['living_time'])
			dct['speed'] = transform_time_to_seconds(dct['speed'])
			dct['validate_date'] = datetime.datetime.strptime(dct['validate_date'], '%y-%m-%d %H:%M')
			return dct

		#正式开始解析
		for item in self._parse_items(response, xpath, attr_map, ProxyItem, post_handler):
			yield item

def main():
	from NetworkService import NetworkService
	from Dispatcher import Dispatcher
	from BaseHandler import BaseItemHandler
	from Handlers.SqlItemHandler import SqlItemHandler
	net = NetworkService()
	dispatcher = Dispatcher()
	dispatcher.set_network_service(net)
	dispatcher.add_item_handler(BaseItemHandler())
	dispatcher.add_item_handler(SqlItemHandler())

	dispatcher.run(ProxySpiderTest())

if __name__ == '__main__':
	main()
