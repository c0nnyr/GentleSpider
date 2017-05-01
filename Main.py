# coding:utf-8
from NetworkService import NetworkService
from Dispatcher import Dispatcher
from Handlers import SqlItemHandler, StatisticItemHandler, LianjiaValidateWarnResponseHandler, RandomWaitRequestHandler
from BaseHandler import BaseItemHandler
from Spiders import DealSpider, HouseSpider, CommunitySpider
from Logger import Logger
from Analyze import DealAnalyzer
import optparse, logging, datetime, json
import GlobalMethod as M

def community(dispatcher, city):
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

def deal(dispatcher, city):
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.add_item_handler(StatisticItemHandler.StatisticItemHandler())

	dispatcher.add_response_handler(LianjiaValidateWarnResponseHandler.LianjiaValidateWarnResponseHandler())

	dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())

	dispatcher.set_config({
		'mode':dispatcher.DEPTH_MODE,
		'use_proxy':False,
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
		'use_proxy':False,
	})
	dispatcher.run(HouseSpider.HouseSpider(city))

def analyze_deal():
	analyzer = DealAnalyzer.DealAnalyzer()
	analyzer.run()

def test(dispatcher, ):
	dispatcher.remove_all_handlers()

	dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
	dispatcher.run(DoubanSpider.DoubanSpider())

def post_handle():
	from Spiders.CommunitySpider import _Model, CommunityStateItem
	import collections, pprint
	session = M.create_engine('community', _Model, prefix='data', suffix='hz2')
	session2 = M.create_engine('community', _Model, prefix='data', suffix='hz')
	#today = M.get_today()
	#yesterday = M.get_today(-1)
	#today_total_count = session.query(HouseStateItem).filter(HouseStateItem.meta_start_date==today).count()
	#print 'house_state_item_count', today, today_total_count
	#print 'house_state_item_count', yesterday, session.query(HouseStateItem).filter(HouseStateItem.meta_start_date==yesterday).count()

	#statistic = collections.defaultdict(lambda :0)
	#statistic_2 = {}

	#for ind, item in enumerate(session.query(HouseStateItem).filter(HouseStateItem.meta_start_date==today)):
	#	yesterday_item = session.query(HouseStateItem).filter(HouseStateItem.meta_start_date==yesterday, HouseStatjeItem.url==item.url).first()
	#	if yesterday_item and yesterday_item.total_price != item.total_price:
	#		#print '{}/{}'.format(ind, today_total_count),
	#		delta = float(item.total_price) - float(yesterday_item.total_price)
	#		#print delta, item.url
	#		key = 'up' if delta > 0 else 'down'
	#		statistic[key] += 1
	#		statistic_2[item.url] = (item, delta)

	#print statistic
	#for item, delta in sorted(statistic_2.itervalues(), key=lambda x:x[1], reverse=True):
	#	print delta, item.url, item.total_price

	for ind, item in enumerate(session.query(CommunityStateItem).all()):
		#item.meta_start_date = item.meta_start_date + datetime.timedelta(days=365*2001 + 120)
		new_item = CommunityStateItem(
			meta_start_date = item.meta_start_date,
			meta_district = item.meta_district,
			meta_price_level = item.meta_price_level,
			url = item.url,

			sale_info = item.sale_info,
			rent_info = item.rent_info,
			unit_price = item.unit_price,
			on_sale_count = item.on_sale_count,
		)
		session2.add(new_item)
		if ind % 3000 == 1:
			print ind
			session2.commit()
	session2.commit()



if __name__ == '__main__':
	Logger()
	dispatcher = Dispatcher()
	dispatcher.set_network_service(NetworkService())

	parser = optparse.OptionParser()
	parser.add_option('-C', '--city', action='store', dest='city', help='set city')
	parser.add_option('-c', '--community_spider', action='store_true', dest='community_spider', help='enable spider of all community')
	parser.add_option('-d', '--deal_spider', action='store_true', dest='deal_spider', help='enable spider of deal')
	parser.add_option('-H', '--house_spider', action='store_true', dest='house_spider', help='enable spider of house')
	parser.add_option('-a', '--analyze_deal', action='store_true', dest='analyze_deal', help='enable analyze deal')
	parser.add_option('-m', '--music', action='store', dest='music', help='play music when end')
	parser.add_option('-P', '--post_handle', action='store_true', dest='post_handle', help='enable post handle')
	parser.add_option('-t', '--test', action='store_true', dest='test', help='enable test')
	options, args = parser.parse_args()
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

	dispatcher.destroy()

