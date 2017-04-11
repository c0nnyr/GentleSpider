# coding:utf-8
import requests, urllib, urllib2
from BaseObject import BaseObject

class NetworkService(BaseObject):
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

	def get(self, url):
		return self.session.get(url)

	def post(self, url, data=None):
		return self.session.post(url, data)
