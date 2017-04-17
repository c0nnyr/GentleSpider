# coding:utf-8
from Items import ProxyItem
from Items import session as db
import requests

def main():
	items = db.query(ProxyItem).filter(ProxyItem.http_type=='HTTP').all()
	s = requests.session()
	s.keep_alive = False
	for item in items:
		try:
			#print item.__dict__
			print '*'*20
			proxies = {'http':'{}:{}'.format(item.ip, item.port)}
			print item.http_type, item.ip, item.port
			response = s.get('http://www.whatismyip.com.tw/', proxies=proxies, timeout=10)
			print response.content
		except Exception as ex:
			print ex

if __name__ == '__main__':
	main()
