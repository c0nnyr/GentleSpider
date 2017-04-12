# coding:utf-8
import requests, urllib, urllib2
from BaseObject import BaseObject
from Response import Response

class NetworkService(BaseObject):
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
		self.session = session = requests.Session()
		session.headers.update(self.DEFAULT_HEADER)

	def send_request(self, request):
		if request.method == 'post':
			r = self.session.post(request.url, request.data)
		elif request.method == 'get':
			r = self.session.get(request.url)
		else:
			raise NotImplementedError()
		resp = Response(body=r.content, url=r.url, status=r.status_code, request_response=r, meta=request.meta)
		request.destroy()


