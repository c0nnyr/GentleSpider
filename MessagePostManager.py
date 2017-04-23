# coding:utf-8
import requests, logging

class MessagePostManager(object):

	@staticmethod
	def post_immediatly(content, title=None):
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
		logging.info('post message response {}'.format(content))
