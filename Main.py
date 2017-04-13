# coding:utf-8
from NetworkService import NetworkService
from Dispatcher import Dispatcher
from BaseItemHandler import BaseItemHandler
from Handlers import SqlHandler
from Spiders import CommunitySpider
from Logger import Logger

def main():
	Logger()
	net = NetworkService()
	dispatcher = Dispatcher()
	dispatcher.set_network_service(net)

	dispatcher.set_item_handler(SqlHandler.SqlHandler())
	dispatcher.run(CommunitySpider.CommunitySpider())

if __name__ == '__main__':
	main()



