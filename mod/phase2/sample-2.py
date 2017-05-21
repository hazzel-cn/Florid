# coding=utf-8

import lib.common

MODULE_NAME = 'sample-2'


def init():
    pass
    # write info into common.SHARING_DICTIONARY


def run(url_obj):
    if 'comment' in url_obj.value and '7' in url_obj.value:
        lib.common.RESULT_DIRECROTY[MODULE_NAME].append(url_obj.value)
    lib.common.CHECKED_COUNT[MODULE_NAME] += 1
    lib.common.ALL_DOWN_COUNT += 1
