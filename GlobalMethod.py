# coding:utf-8
import functools, traceback, sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, create_engine, and_, or_, DateTime
import datetime, types

def create_db_engine(db_name):
	engine = create_engine('sqlite:///{}.sqlite'.format(db_name))
	session = sessionmaker(bind=engine)()
	Model = declarative_base(name=db_name)
	return engine, session, Model

def arg_to_iter(arg):
	if arg is None:
		return []
	elif isinstance(arg, (list, tuple)):
		return arg
	elif isinstance(arg, types.GeneratorType):
		return list(arg)
	else:
		return [arg]

def check_validate_auto_redirect(func):
	@functools.wraps(func)
	def _func(self, response):
		need_validate = False
		for r in self.try_validate(response, func.__name__):
			need_validate = True
			yield r
		if not need_validate:
			for r in arg_to_iter(func(self, response)):
				yield r
	return _func

def fill_meta_extract_start_urls(base_url, base_metas):
	start_urls = [base_url.format(page='', **meta) for meta in base_metas]
	for start_url, meta in zip(start_urls, base_metas):
		meta['start_url'] = start_url
		meta['start_date'] = get_today_str()
	return start_urls

def get_today_str(delta=0):
	return (datetime.date.today() + datetime.timedelta(delta)).strftime('%y-%m-%d')

def draw_hist(x, x_lable='', y_lable='', title='', bin_count=50):
	import numpy as np
	import matplotlib.mlab as mlab
	import matplotlib.pyplot as plt
	fig, ax = plt.subplots()
	n, bins, patches = ax.hist(x, bin_count, normed=1)

	#ax.plot(bins, y, '--')
	ax.set_xlabel(x_lable)
	ax.set_ylabel(y_lable)
	ax.set_title(title)

	# Tweak spacing to prevent clipping of ylabel
	#fig.tight_layout()
	plt.show()


def auto_inc():
	return sys._getframe(1).f_lineno

if __name__ == '__main__':
	print auto_inc()
	import os
	if not os.path.exists('a/b/c'):
		os.makedirs('a/b/c')


