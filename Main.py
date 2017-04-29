# coding:utf-8
from NetworkService import NetworkService
from Dispatcher import Dispatcher
from Handlers import SqlItemHandler, StatisticItemHandler, LianjiaValidateWarnResponseHandler, RandomWaitRequestHandler
from BaseHandler import BaseItemHandler
from Spiders import DealSpider, HouseSpider, CommunitySpider
from Logger import Logger
from Analyze import DealAnalyzer
import optparse, logging, datetime, json

Logger()
net = NetworkService()
dispatcher = Dispatcher()
dispatcher.set_network_service(net)

def community(city):
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_response_handler(LianjiaValidateWarnResponseHandler.LianjiaValidateWarnResponseHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.set_config({
		'mode':dispatcher.DEPTH_MODE,
		'use_proxy':False,
	})
	dispatcher.run(CommunitySpider.CommunitySpider(city))

def deal(city):
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_response_handler(LianjiaValidateWarnResponseHandler.LianjiaValidateWarnResponseHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.set_config({
		'mode':dispatcher.DEPTH_MODE,
		'use_proxy':True,
		'use_cache':True,
		'need_check_existence':False,
	})

	dispatcher.run(DealSpider.DealSpider(city))

def house():
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_response_handler(LianjiaValidateWarnResponseHandler.LianjiaValidateWarnResponseHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.set_config({
		'mode':dispatcher.DEPTH_MODE,
		'use_proxy':True,
	})
	dispatcher.run(HouseSpider.HouseSpider())

def analyze_deal():
	analyzer = DealAnalyzer.DealAnalyzer()
	analyzer.run()

def test():
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.run(DoubanSpider.DoubanSpider())

def post_handle():
	pass

if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('-c', '--community_spider', action='store', dest='community_spider', help='enable spider of all community')
	parser.add_option('-d', '--deal_spider', action='store', dest='deal_spider', help='enable spider of deal')
	parser.add_option('-H', '--house_spider', action='store_true', dest='house_spider', help='enable spider of house')
	parser.add_option('-a', '--analyze_deal', action='store_true', dest='analyze_deal', help='enable analyze deal')
	parser.add_option('-m', '--music', action='store', dest='music', help='play music when end')
	parser.add_option('-P', '--post_handle', action='store_true', dest='post_handle', help='enable post handle')
	parser.add_option('-t', '--test', action='store_true', dest='test', help='enable test')
	options, args = parser.parse_args()
	if options.community_spider:
		logging.info('using community spider')
		community(options.community_spider)
	if options.house_spider:
		logging.info('using house spider')
		house()
	if options.deal_spider:
		logging.info('using deal spider')
		deal(options.deal_spider)
	if options.analyze_deal:
		logging.info('using analyze deal')
		analyze_deal()
	if options.post_handle:
		logging.info('using post_handle ')
		post_handle()
	if options.test:
		logging.info('using test')
		test()

	if options.music:
		import os
		os.system('play ' + options.music)

