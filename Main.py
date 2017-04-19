# coding:utf-8
from NetworkService import NetworkService
from Dispatcher import Dispatcher
from Handlers import SqlItemHandler, StatisticItemHandler, LianjiaValidateWarnResponseHandler, RandomWaitRequestHandler
from Spiders import CommunitySpider, ProxySpider, DealSpider, HouseSpider
from Logger import Logger
import optparse, logging

Logger()
net = NetworkService()
dispatcher = Dispatcher()
dispatcher.set_network_service(net)

def community():
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_response_handler(LianjiaValidateWarnResponseHandler.LianjiaValidateWarnResponseHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.enable_score_proxy(True)
	dispatcher.enable_use_proxy(True)
	dispatcher.run(CommunitySpider.CommunitySpider())

def proxy():
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.enable_score_proxy(False)
	dispatcher.enable_use_proxy(False)
	dispatcher.run(ProxySpider.ProxySpider2())
	dispatcher.run(ProxySpider.ProxySpider1())

def deal():
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_response_handler(LianjiaValidateWarnResponseHandler.LianjiaValidateWarnResponseHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.enable_score_proxy(True)
	dispatcher.enable_use_proxy(True)
	dispatcher.run(DealSpider.DealSpider())

def house():
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_response_handler(LianjiaValidateWarnResponseHandler.LianjiaValidateWarnResponseHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.enable_score_proxy(True)
	dispatcher.enable_use_proxy(True)
	dispatcher.run(HouseSpider.HouseSpider())

if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('-p', '--proxy_spider', action='store_true', dest='proxy_spider', help='enable spider of proxy')
	parser.add_option('-c', '--community_spider', action='store_true', dest='community_spider', help='enable spider of all community')
	parser.add_option('-d', '--deal_spider', action='store_true', dest='deal_spider', help='enable spider of deal')
	parser.add_option('-H', '--house_spider', action='store_true', dest='house_spider', help='enable spider of house')
	options, args = parser.parse_args()
	if options.proxy_spider:
		logging.info('using proxy spider')
		proxy()
	if options.community_spider:
		logging.info('using community spider')
		community()
	if options.house_spider:
		logging.info('using house spider')
		house()




