# coding:utf-8
from BaseSpider import BaseSpider

class LianjiaSider(BaseSpider):
	RESBLOCK_URL = 'http://cd.lianjia.com/ershoufang/{page}c{rid}/'
	COMMUNITY_ITEM_INFO_RE = r'''require\(\['ershoufang/sellList/index'\],\s*?function\s*?\(main\)\s*?\{\s*?main\((?P<extract>(\s|\S)*?)\);\s*?\}\);'''
	def __init__(self):
		super(LianjiaSider, self).__init__()
		rid = 1611041529992#望江嘉园
		self.start_urls = (self.RESBLOCK_URL.format(rid=rid, page=''), )

	def parse(self, response):
		print response.url
		print response.re(self.COMMUNITY_ITEM_INFO_RE)
		house_url_xpath = '/html/body/div[4]/div[1]/ul/li/div[1]/div[1]/a/@href'
		for url in response.xpath(house_url_xpath).extract():
			print url

def main():
	from NetworkService import NetworkService
	from Dispatcher import Dispatcher
	from BaseItemHandler import BaseItemHandler
	net = NetworkService()
	dispatcher = Dispatcher()
	item_handler = BaseItemHandler()
	dispatcher.set_network_service(net)
	dispatcher.set_item_handler(item_handler)

	dispatcher.run(LianjiaSider())

if __name__ == '__main__':
	main()
