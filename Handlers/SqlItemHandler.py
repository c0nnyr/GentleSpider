# coding:utf-8

from BaseHandler import BaseItemHandler
import SqlDBHelper
import logging

class SqlItemHandler(BaseItemHandler):

	def handle(self, item):
		db = item.db
		#check_primary_existence = getattr(item, 'check_existence', None)
		#if check_primary_existence:
		#	if check_primary_existence():
		#		logging.info('***************\nalready existed\nnew {}\n'.format(item.__dict__, ))

		db.merge(item)
		db.commit()
