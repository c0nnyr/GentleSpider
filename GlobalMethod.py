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
