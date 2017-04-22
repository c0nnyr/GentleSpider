# coding:utf-8
import functools

def is_item(arg):
	return getattr(arg.__class__, 'IS_ITEM', False)

def arg_to_iter(arg):
	if arg is None:
		return []
	elif not getattr(arg.__class__, 'IS_ITEM', False) and hasattr(arg, '__iter__'):
		return arg
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
		meta['page'] = 1
	return start_urls

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
	fig.tight_layout()
	plt.show()


