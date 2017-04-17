# coding:utf-8
from NetworkService import NetworkService
from Dispatcher import Dispatcher
from Handlers import SqlItemHandler, StatisticItemHandler, LianjiaValidateWarnResponseHandler, RandomWaitRequestHandler
from BaseHandler import BaseItemHandler
from Spiders import CommunitySpider, ProxySpider
from Logger import Logger

def main():
	Logger()
	net = NetworkService()
	dispatcher = Dispatcher()
	dispatcher.set_network_service(net)

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())
	#dispatcher.add_response_handler(LianjiaValidateWarnResponseHandler.LianjiaValidateWarnResponseHandler())
	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	#dispatcher.run(CommunitySpider.CommunitySpider())
	dispatcher.run(ProxySpider.ProxySpider())

def proxy():
	Logger()
	net = NetworkService()
	dispatcher = Dispatcher()
	dispatcher.set_network_service(net)

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())
	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.run(ProxySpider.ProxySpider())

if __name__ == '__main__':
	#main()
	proxy()




