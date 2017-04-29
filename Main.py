# coding:utf-8
from NetworkService import NetworkService
from Dispatcher import Dispatcher
from Handlers import SqlItemHandler, StatisticItemHandler, LianjiaValidateWarnResponseHandler, RandomWaitRequestHandler
from BaseHandler import BaseItemHandler
from Spiders import DealSpider, HouseSpider
from Logger import Logger
from Analyze import DealAnalyzer
import optparse, logging, datetime, json

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
		'use_proxy':True,
	})
	dispatcher.run(CommunitySpider.CommunitySpider())

def proxy(spider_ids):
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.set_config({
		'mode':dispatcher.DEPTH_MODE,
		'use_proxy':False,
	})
	ids = [int(_id) for _id in spider_ids.split(',')]
	spider_cls = [ProxySpider.ProxySpider1, ProxySpider.ProxySpider2, ProxySpider.ProxySpider3, ProxySpider.ProxySpider4,]
	spiders = [spider_cls[_id - 1]() for _id in ids]
	dispatcher.run(*spiders)

def deal(city):
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_response_handler(LianjiaValidateWarnResponseHandler.LianjiaValidateWarnResponseHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.set_config({
		'mode':dispatcher.DEPTH_MODE,
		'use_proxy':False,
		'use_cache':False,
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
	import Items
	merge_count = 0
	db2 = Items.DealItem2.db
	db = Items.DealItem.db
	import re
	sum_count = 0
	for ind, item in enumerate(db2.query(Items.DealItem2).all()):
		print ind
		new_item = Items.DealItem(
			_crawl_date = item._crawl_date,
			meta_district = item.meta_district,
			meta_area = item.meta_area,
			meta_price_level = item.meta_price_level,
			meta_start_url = item.meta_start_url,

			url = item.url,
			deal_id = item.deal_id,
			deal_date = item.deal_date,
			title = item.title,
			house_info = item.house_info,
			total_price = item.total_price,
			position_info = item.position_info,
			deal_platform = item.deal_platform,
			unit_price = item.unit_price,
			deal_house_text = item.deal_house_text,
			deal_cycle_txt = item.deal_cycle_txt,
		)
		db.add(new_item)
		sum_count += 1
		if sum_count > 5000:
			sum_count = 0
			db.commit()
	db.commit()

if __name__ == '__main__':
	parser = optparse.OptionParser()
	parser.add_option('-p', '--proxy_spider', action='store', dest='proxy_spider', help='enable spider of proxy')
	parser.add_option('-c', '--community_spider', action='store_true', dest='community_spider', help='enable spider of all community')
	parser.add_option('-d', '--deal_spider', action='store', dest='deal_spider', help='enable spider of deal')
	parser.add_option('-H', '--house_spider', action='store_true', dest='house_spider', help='enable spider of house')
	parser.add_option('-a', '--analyze_deal', action='store_true', dest='analyze_deal', help='enable analyze deal')
	parser.add_option('-m', '--music', action='store', dest='music', help='play music when end')
	parser.add_option('-P', '--post_handle', action='store_true', dest='post_handle', help='enable post handle')
	parser.add_option('-t', '--test', action='store_true', dest='test', help='enable test')
	options, args = parser.parse_args()
	if options.proxy_spider:
		logging.info('using proxy spider')
		proxy(options.proxy_spider)
	if options.community_spider:
		logging.info('using community spider')
		community()
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

