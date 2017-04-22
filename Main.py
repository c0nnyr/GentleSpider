# coding:utf-8
from NetworkService import NetworkService
from Dispatcher import Dispatcher
from Handlers import SqlItemHandler, StatisticItemHandler, LianjiaValidateWarnResponseHandler, RandomWaitRequestHandler
from Spiders import CommunitySpider, ProxySpider, DealSpider, HouseSpider
from Logger import Logger
from Analyze import DealAnalyzer
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

	dispatcher.set_config({
		'mode':dispatcher.DEPTH_MODE,
		'score_proxy':True,
		'use_proxy':True,
	})
	dispatcher.run(CommunitySpider.CommunitySpider())

def proxy():
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.set_config({
		'mode':dispatcher.DEPTH_MODE,
		'score_proxy':False,
		'use_proxy':False,
	})
	dispatcher.run(ProxySpider.ProxySpider2())
	dispatcher.run(ProxySpider.ProxySpider1())

def deal():
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_response_handler(LianjiaValidateWarnResponseHandler.LianjiaValidateWarnResponseHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.set_config({
		'mode':dispatcher.DEPTH_MODE,
		'score_proxy':False,
		'use_proxy':False,
	})

	dispatcher.run(DealSpider.DealSpider())

def house():
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_response_handler(LianjiaValidateWarnResponseHandler.LianjiaValidateWarnResponseHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.set_config({
		'mode':dispatcher.DEPTH_MODE,
		'score_proxy':True,
		'use_proxy':True,
	})
	dispatcher.run(HouseSpider.HouseSpider())

def analyze_deal():
	analyzer = DealAnalyzer.DealAnalyzer()
	analyzer.run()

if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('-p', '--proxy_spider', action='store_true', dest='proxy_spider', help='enable spider of proxy')
	parser.add_option('-c', '--community_spider', action='store_true', dest='community_spider', help='enable spider of all community')
	parser.add_option('-d', '--deal_spider', action='store_true', dest='deal_spider', help='enable spider of deal')
	parser.add_option('-H', '--house_spider', action='store_true', dest='house_spider', help='enable spider of house')
	parser.add_option('-a', '--analyze_deal', action='store_true', dest='analyze_deal', help='enable analyze deal')
	parser.add_option('-m', '--music', action='store', dest='music', help='play music when end')
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
	if options.deal_spider:
		logging.info('using deal spider')
		deal()
	if options.analyze_deal:
		logging.info('using analyze deal')
		analyze_deal()
	if options.music:
		import os
		os.system('play ' + options.music)
