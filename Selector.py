# coding:utf-8
from lxml import etree, html
import types, re
from w3lib.html import replace_entities

def flatten(lst):
	return list(iflatten(lst))
def iflatten(lst):
	for el in lst:
		if hasattr(el, '__iter__') and not isinstance(el, types.StringTypes):
			for el2 in iflatten(el):
				yield el2
		else:
			yield el

class SelectorList(object):
	def __init__(self, selector_lst):
		self.selector_lst = selector_lst

	def re(self, regex):
		return flatten(sel.re(regex) for sel in self.selector_lst)

	def re_first(self, regex, defualt=None):
		for el in iflatten(sel.re(regex) for sel in self.selector_lst):
			return el
		return defualt

	def xpath(self, query, **kwargs):
		return flatten(sel.xpath(query, **kwargs) for sel in self.selector_lst)

	def xpath_first(self, query, default=None, **kwargs):
		for el in iflatten(sel.xpath(query, **kwargs) for sel in self.selector_lst):
			return el
		return default

	def extract(self):
		return [sel.extract() for sel in self.selector_lst]

	def extract_first(self, default=None):
		for sel in self.selector_lst:
			return sel.extract()
		return default

	def __bool__(self):
		return bool(self.selector_lst)
	__nonzero__ = __bool__

class Selector(object):
	ENCODING_TYPE = 'utf8'
	def __init__(self, text=None, root=None, type='html', expr=''):
		PARSER_CLS_MAP = {
			'html':html.HTMLParser,
			'xml':etree.XMLParser
		}
		self.SELECTOR_LIST_CLS = SelectorList
		self.expr = expr
		self.type = type

		if text is not None:
			parser_cls = PARSER_CLS_MAP[type]
			def create_root(text=text, parser_cls=parser_cls):
				if not isinstance(text, str):
					text = text.encode(self.ENCODING_TYPE)
				body = text.strip() or '<html/>'
				parser = parser_cls(recover=True, encoding=self.ENCODING_TYPE)
				return etree.fromstring(body, parser=parser)
			root = create_root()
		self.root = root

	def re(self, regex):
		if isinstance(regex, types.StringTypes):
			regex = re.compile(regex, re.UNICODE)
		text = self.extract()
		try:
			lst = [regex.search(text).group('extract')]
		except:
			lst = regex.findall(text)
		return [replace_entities(s, keep=['lt', 'amp']) for s in flatten(lst)]

	def xpath(self, query, *args, **kwargs):
		result = self.root.xpath(query, smart_strings=False, **kwargs)
		if not isinstance(result, list):
			result = [result]
		result = [self.__class__(root=x, type=self.type, expr=query) for x in result]
		return self.SELECTOR_LIST_CLS(result)

	def extract(self):
		try:
			return etree.tostring(self.root, method=self.type, encoding=self.ENCODING_TYPE, with_tail=False)
		except (AttributeError, TypeError):
			return self.root.decode(self.ENCODING_TYPE)

	def __bool__(self):
		return bool(self.extract())
	__nonzero__ = __bool__

	def __str__(self):
		data = repr(self.extract()[:40])
		return "<%s xpath=%r data=%s>" % (type(self).__name__, self.expr, data)
	__repr__ = __str__
