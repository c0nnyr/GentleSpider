# coding:utf-8

import logging

class Logger(object):
	def __init__(self):
		logging.basicConfig(level=logging.DEBUG,
							format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
							datefmt='%a, %d %b %Y %H:%M:%S', )

		#console = logging.StreamHandler()
		#console.setLevel(logging.INFO)
		#formatter = logging.Formatter('%(asctime)-20s %(message)s')
		#console.setFormatter(formatter)
		#logging.getLogger('').addHandler(console)