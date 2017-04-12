# coding:utf-8
from NetworkService import NetworkService
from Dispatcher import Dispatcher
from BaseItemHandler import BaseItemHandler
from BaseSpider import BaseSpider

def main():
	net = NetworkService()
	dispatcher = Dispatcher()
	item_handler = BaseItemHandler()
	dispatcher.set_network_service(net)
	dispatcher.set_item_handler(item_handler)

	dispatcher.run(BaseSpider())

if __name__ == '__main__':
	main()



