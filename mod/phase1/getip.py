# coding=utf-8
import socket

import lib.colorprint
import lib.common
import lib.urlentity

MODULE_NAME = 'getip'


def init():
    pass
    # write info into common.SHARING_DICTIONARY


def run():
    url_obj = lib.urlentity.URLEntity(raw_url=lib.common.SOURCE_URL)
    lib.common.RESULT_DIRECROTY[MODULE_NAME].append('IP: ' + socket.gethostbyname(url_obj.hostname))
