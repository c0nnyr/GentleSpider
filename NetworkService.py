# coding:utf-8
import requests
from Response import Response
import logging

class NetworkService(object):
	#取自chrome的一次访问
	DEFAULT_HEADER = {
		'Connection': 'keep-alive',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
	}
	def __init__(self):
		super(NetworkService, self).__init__()
		self.session = None
		self.cur_proxies = None

	def _update_session(self, proxies):
		if proxies != self.cur_proxies:
			if self.session:
				self.session.close()
				self.session = None
		if not self.session:
			self.session = session = requests.Session()
			session.headers.update(self.DEFAULT_HEADER)
			session.keep_alive = False
			self.cur_proxies = proxies
		#requests.adapters.DEFAULT_RETRIES = 5

	def clear(self):
		if self.session:
			self.session.close()
			self.session = None
		self.cur_proxies = None

	def send_request(self, request, **kwargs):
		logging.info('Requesting {}'.format(request))
		self._update_session(kwargs.get('proxies'))

		if request.method == 'post':
			r = self.session.post(request.url, request.data, **kwargs)
		elif request.method == 'get':
			r = self.session.get(request.url, **kwargs)
		else:
			raise NotImplementedError()
		return Response(body=r.content, url=r.url, status=r.status_code, meta=request.meta)



