# coding:utf-8
from Selector import Selector

class Response(object):

    def __init__(self, body, url='', meta=None, status=-1, request_response=None):
        self._status = int(status)
        self._url = url
        self._body = body
        self._request_response = request_response
        self._selector = Selector(body)
        self._meta = meta or {}

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

    def xpath(self, query, **kwargs):
        return self._selector.xpath(query, **kwargs)

    def re(self, regex):
        return self._selector.re(regex)

