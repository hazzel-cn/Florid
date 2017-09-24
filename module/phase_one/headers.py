import requests

import lib.common

MODULE_NAME = 'headers'


def run():
    r = requests.get(lib.common.SOURCE_URL)

    # X-Forwarded-By:
    if 'X-Powered-By' in r.headers:
        lib.common.RESULT_ONE_DICT['X-Powered-By'] = r.headers['X-Powered-By']

    # Server:
    if 'Server' in r.headers:
        lib.common.RESULT_ONE_DICT['Server'] = r.headers['Server']

    lib.common.ALIVE_LINE[MODULE_NAME] += 1
