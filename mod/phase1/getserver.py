# coding=utf-8

import requests

import lib.common

MODULE_NAME = 'getserver'


def init():
    pass
    # write info into common.SHARING_DICTIONARY


def run():
    url_obj = lib.urlentity.URLEntity(raw_url=lib.common.SOURCE_URL)
    response_obj = requests.get(url_obj.value)
    headers = response_obj.headers
    try:
        lib.common.RESULT_DIRECROTY[MODULE_NAME].append('Server: ' + headers['Server'])
    except Exception, noServerInfo:
        pass
        # print 'Sample'
