# coding=utf-8

import lib.common

MODULE_NAME = 'sample-1'


def init():
    pass
    # write info into common.SHARING_DICTIONARY


def run():
    # print '1-sample is running', url_obj
    lib.common.RESULT_DIRECROTY[MODULE_NAME].append('this is a sample in phase one')
    # print 'Sample'
