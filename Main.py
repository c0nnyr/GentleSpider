# coding:utf-8
from NetworkService import NetworkService
import requests
if __name__ == '__main__':
	net = NetworkService()
	res = requests.get('http://baidu.com')
	print res.text



