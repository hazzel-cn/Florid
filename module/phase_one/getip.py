import socket

import lib.common
import lib.urlentity

MODULE_NAME = 'getip'


def run():
    ip = socket.gethostbyname(lib.urlentity.URLEntity(lib.common.SOURCE_URL).get_hostname())
    lib.common.RESULT_ONE_DICT['Ip Addr'] = str(ip)
    lib.common.ALIVE_LINE[MODULE_NAME] += 1
