
# coding:utf-8
import requests, logging

DEVICE_ID = 'u-3341c1e1-cd92-495f-a9f1-38d09e0c'

def post(content, title=None):
	if title is None:title = content
	logging.info('posting message content:{}, title {}'.format(content, title))
	requests.post(
		'https://api.alertover.com/v1/alert',
		data={
			'source': DEVICE_ID,
			'receiver': DEVICE_ID,
			'content': content,
			'title': title,
		}
	)

if __name__ == '__main__':
	post('total items {}'.format(100))

