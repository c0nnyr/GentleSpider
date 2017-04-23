# coding:utf-8
import requests, logging

DEVICE_ID = 'u-3341c1e1-cd92-495f-a9f1-38d09e0c'

def post(content, title=None):
	if title is None:title = content
	logging.info('posting message content:{}, title {}'.format(content, title))
	response = requests.post(
		'https://api.alertover.com/v1/alert',
		data={
			'source': 's-51a420f0-8eb2-4a28-a568-43064e78',
			'receiver': 'g-e6fd7ced-fd5c-421d-8bc0-a995951d',
			'content': content,
			'title': title,
		}
	)
	#print response.content

if __name__ == '__main__':
	post('total items {}'.format(200))

