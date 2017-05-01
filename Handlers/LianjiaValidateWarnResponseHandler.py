# coding:utf-8

from BaseHandler import BaseResponseHandler

class LianjiaValidateWarnResponseHandler(BaseResponseHandler):

	def __init__(self):
		super(LianjiaValidateWarnResponseHandler, self).__init__()
		self.validate_count = 0

	def handle(self, response, spider):
		if 'captcha.lianjia.com/' in response.url:
			self.validate_count += 1
		if self.validate_count > 500:
			raise Exception('LianjiaValidateWarnResponseHandler ends spider')
