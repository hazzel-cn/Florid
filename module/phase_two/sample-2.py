import lib.common
import time

MODULE_NAME = 'sample-2'


def init():
    pass


def run(url):
    time.sleep(1)
    if '1' in url:
        lib.common.RESULT_DICT[MODULE_NAME].append(url)
    lib.common.ALIVE_LINE[MODULE_NAME] += 1
