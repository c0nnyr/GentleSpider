# coding:utf-8
from NetworkService import NetworkService
from Dispatcher import Dispatcher
from Handlers import SqlItemHandler, StatisticItemHandler, LianjiaValidateWarnResponseHandler, RandomWaitRequestHandler
from BaseHandler import BaseItemHandler
from Spiders import DealSpider, HouseSpider, CommunitySpider, DoubanSpider, NewCommunitySpider
from Logger import Logger
from Analyze import DealAnalyzer
import optparse, logging, datetime, json
import GlobalMethod as M

def new_community(dispatcher, city):
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_response_handler(LianjiaValidateWarnResponseHandler.LianjiaValidateWarnResponseHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.set_config({
		'mode':dispatcher.DEPTH_MODE,
		'use_proxy':True,
	})
	dispatcher.run(NewCommunitySpider.NewCommunitySpider(city))

def community(dispatcher, city):
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_response_handler(LianjiaValidateWarnResponseHandler.LianjiaValidateWarnResponseHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.set_config({
		'mode':dispatcher.DEPTH_MODE,
		'use_proxy':True,
	})
	dispatcher.run(CommunitySpider.CommunitySpider(city))

def deal(dispatcher, city):
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_response_handler(LianjiaValidateWarnResponseHandler.LianjiaValidateWarnResponseHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.set_config({
		'mode':dispatcher.DEPTH_MODE,
		'use_proxy':True,
		'need_check_existence':True,
	})

	dispatcher.run(DealSpider.DealSpider(city))

def house(dispatcher, city):
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_response_handler(LianjiaValidateWarnResponseHandler.LianjiaValidateWarnResponseHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.set_config({
		'mode':dispatcher.DEPTH_MODE,
		'use_proxy':True,
	})
	dispatcher.run(HouseSpider.HouseSpider(city))

def analyze_deal():
	analyzer = DealAnalyzer.DealAnalyzer()
	analyzer.run()

def book(dispatcher, ):
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())
	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.set_config({
		'mode':dispatcher.DEPTH_MODE,
		'use_proxy':True,
	})
	dispatcher.run(DoubanSpider.DoubanSpider())

def post_handle():
	from Spiders.HouseSpider import _Model, HouseStateItem, HouseItem
	import collections, pprint
	session = M.create_engine('house', _Model, prefix='data', suffix='cd')
	today = M.get_today(-1)
	yesterday = M.get_today(-3)
	today_total_count = session.query(HouseStateItem).filter(HouseStateItem.meta_start_date==today).count()
	print 'house_state_item_count', today, today_total_count
	print 'house_state_item_count', yesterday, session.query(HouseStateItem).filter(HouseStateItem.meta_start_date==yesterday).count()

	statistic = collections.defaultdict(lambda :0)
	statistic_2 = {}

	for ind, item in enumerate(session.query(HouseStateItem).filter(HouseStateItem.meta_start_date==today)):
		yesterday_item = session.query(HouseStateItem).filter(HouseStateItem.meta_start_date==yesterday, HouseStateItem.url==item.url).first()
		print ind
		if yesterday_item and yesterday_item.total_price != item.total_price:
			#print '{}/{}'.format(ind, today_total_count),
			delta = float(item.total_price) - float(yesterday_item.total_price)
			#print delta, item.url
			key = 'up' if delta > 0 else 'down'
			statistic[key] += 1
			statistic_2[item.url] = (item, delta, session.query(HouseItem.title).filter(HouseItem.url == item.url).first())

	print statistic
	for item, delta, title in sorted(statistic_2.itervalues(), key=lambda x:x[1], reverse=True):
		print delta, item.url, item.total_price,
		print title[0]

if __name__ == '__main__':
	Logger()
	parser = optparse.OptionParser()
	parser.add_option('-C', '--city', action='store', dest='city', help='set city')
	parser.add_option('-c', '--community_spider', action='store_true', dest='community_spider', help='enable spider of all community')
	parser.add_option('-d', '--deal_spider', action='store_true', dest='deal_spider', help='enable spider of deal')
	parser.add_option('-H', '--house_spider', action='store_true', dest='house_spider', help='enable spider of house')
	parser.add_option('-a', '--analyze_deal', action='store_true', dest='analyze_deal', help='enable analyze deal')
	parser.add_option('-m', '--music', action='store', dest='music', help='play music when end')
	parser.add_option('-P', '--post_handle', action='store_true', dest='post_handle', help='enable post handle')
	parser.add_option('-t', '--test', action='store_true', dest='test', help='enable test')
	parser.add_option('-b', '--book', action='store_true', dest='book', help='enable book')
	parser.add_option('-n', '--new_community', action='store_true', dest='new_community', help='enable new_community')
	parser.add_option('-T', '--tag', action='store', dest='tag', help='tag')
	options, args = parser.parse_args()

	dispatcher = Dispatcher(options.tag or '')
	dispatcher.set_network_service(NetworkService())

	if options.city:
		cities = options.city.split()
	else:
		cities = ('cd', )
	if options.community_spider:
		logging.info('using community spider')
		for city in cities:
			community(dispatcher, city)
	if options.house_spider:
		logging.info('using house spider')
		for city in cities:
			house(dispatcher, city)
	if options.deal_spider:
		logging.info('using deal spider')
		for city in cities:
			deal(dispatcher, city)
	if options.new_community:
		logging.info('using new_community spider')
		for city in cities:
			new_community(dispatcher, city)
	if options.analyze_deal:
		logging.info('using analyze deal')
		analyze_deal()
	if options.post_handle:
		logging.info('using post_handle ')
		post_handle()
	if options.book:
		logging.info('using book')
		book(dispatcher)
	if options.test:
		logging.info('using test')
		test(dispatcher)

	if options.music:
		import os
		os.system('play ' + options.music)

	dispatcher.destroy()

