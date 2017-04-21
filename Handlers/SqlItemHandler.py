# coding:utf-8

from BaseHandler import BaseItemHandler
import SqlDBHelper
import logging

class SqlItemHandler(BaseItemHandler):

	def handle(self, item):
		if isinstance(item, SqlDBHelper.RequestResponseMap):
			from SqlDBHelper import rr_session as db
		elif isinstance(item, SqlDBHelper.ProxyItem):
			from SqlDBHelper import p_session as db
		else:
			from Items import session as db
		#check_primary_existence = getattr(item, 'check_primary_existence', None)
		#if check_primary_existence:
		#	old_item = check_primary_existence(item)
		#	if old_item:
		#		logging.info('***************\nalready existed\nnew {}\nold {}\n'.format(item.__dict__, old_item.__dict__))

		db.merge(item)
		db.commit()
