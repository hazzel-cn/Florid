# coding=utf-8
'''
# filename = sample.py
# phase: 1
'''
import lib.common

MODULE_NAME = str(__file__).split('/')[-1].split('\\')[-1].replace('.pyc', '').replace('.py', '')


def init():
    pass
    # write info into common.SHARING_DICTIONARY


def run(url_obj):

    if 'comment' in url_obj.value and '7' in url_obj.value:
        lib.common.RESULT_DIRECROTY[MODULE_NAME].append(url_obj.value)
    lib.common.CHECKED_COUNT[MODULE_NAME] += 1
    lib.common.ALL_DOWN_COUNT += 1
