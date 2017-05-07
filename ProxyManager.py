# coding:utf-8
from SqlDBHelper import ProxyItem, RequestResponseMap
import itertools, logging, time
from Handlers import SqlItemHandler, RandomWaitRequestHandler
from Spiders import ProxySpider
import GlobalMethod as M

class ProxyManager(object):
	REQUEST_COUNT_THRESHOLD = ProxyItem.DEFAULT_SCORE

	def __init__(self, tag=''):
		self._proxy = None
		self._proxy_score = None
		self._cur_proxy_request_count = 0
		self.session = M.create_engine('proxy' + tag, ProxyItem)

	def destroy(self):
		if self.session:
			self.session.close()
			self.session = None

	def crawl_new_proxies(self, proxy_dispatcher):
		logging.info('crawl_new_proxies now')
		ProxyItem.clear_all(self.session)
		proxy_dispatcher.add_item_handler(SqlItemHandler.SqlItemHandler())
		proxy_dispatcher.add_request_handler(RandomWaitRequestHandler.RandomWaitRequestHandler())
		spiders = [cls() for cls in ProxySpider.cls_list]
		proxy_dispatcher.run(*spiders)

	def pick_proxy(self, url):
		if not self._proxy or self._cur_proxy_request_count > self.REQUEST_COUNT_THRESHOLD:
			self._proxy, self._proxy_score = self._choose_proxy(url)
			logging.info('try using proxy {}'.format(self._proxy))
			self._cur_proxy_request_count = 0
		return self._proxy

	def feed_yes_or_no(self, b):
		if not self._proxy:
			return #不会这里

		if b:
			self._cur_proxy_request_count += 1
		else:
			delta_score = self._get_delta_score()
			self._score_proxy(self._proxy_score + delta_score)#成功多少次就打多少分.所有的一开始是100分,试验一次就知道多少分了
			self._proxy = None#清空

	def _get_delta_score(self):
		if self._cur_proxy_request_count == 1:
			return 0
		elif self._cur_proxy_request_count > 1:
			return int(self._cur_proxy_request_count / 2) #适度加分
		else:
			return -1#减一分

	def _choose_proxy(self, url):
		if url.startswith('https'):
			http_type = 'HTTPS'
		else:
			http_type = 'HTTP'
		return ProxyItem.get_proper_proxy(self.session, http_type)

	def _score_proxy(self, score):
		if self._proxy:
			logging.info('scoring proxy {} score {}'.format(self._proxy, score))
			ProxyItem.set_proxy_score(self.session, self._proxy, score)

