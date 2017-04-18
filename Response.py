# coding:utf-8
from Selector import Selector
import cPickle

class Response(object):

    def __init__(self, body, url='', meta=None, status=-1):
        self._status = int(status)
        self._url = url
        self._body = body
        self._selector = Selector(body)
        self._meta = meta or {}
        self._id = -1

    @property
    def url(self):
        return self._url
    @property
    def body(self):
        return self._body
    @property
    def meta(self):
        return self._meta
    @property
    def status(self):
        return self._status
    @property
    def id(self):
        return self._id

    def dumps(self):
        return cPickle.dumps(dict(url=self.url, status=self.status, body=self.body, meta=self.meta))

    @classmethod
    def loads(cls, s):
        if isinstance(s, unicode):
            s = s.encode('utf-8')
        dct = cPickle.loads(s)
        return cls(**dct)

    def xpath(self, query, **kwargs):
        return self._selector.xpath(query, **kwargs)

    def re(self, regex):
        return self._selector.re(regex)

    def re_first(self, regex):
        try:
            return self._selector.re(regex)[0]
        except:
            return ''

    def set_request_response_id(self, id):
        self._id = id
